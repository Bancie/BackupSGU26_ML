"""MCP server: semantic search over parsed EDA book markdown via FAISS + sentence-transformers."""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_THIS_DIR = Path(__file__).resolve().parent
_here_resolved = _THIS_DIR.resolve()


def _path_is_here(entry: str) -> bool:
    try:
        return Path(entry).resolve() == _here_resolved
    except OSError:
        return False


# Repo has a folder named `mcp/`; when running `python mcp/eda.py`, that directory is on sys.path first
# and shadows the PyPI package `mcp`. Drop script dir entries so MCP SDK resolves correctly.
sys.path[:] = [entry for entry in sys.path if not _path_is_here(entry)]

import faiss
import numpy as np
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

_DEFAULT_MODEL = "all-MiniLM-L6-v2"
_MAX_CHUNK = 2500
_OVERLAP = 200
_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_CORPUS = _REPO_ROOT / "parsing" / "eda_withpython_suresh_kumar"


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _corpus_dir() -> Path:
    raw = os.environ.get("EDA_CORPUS_DIR", "").strip()
    return Path(raw).expanduser().resolve() if raw else _DEFAULT_CORPUS


def _source_path() -> Path:
    return _corpus_dir() / "parsing.md"


def _cache_dir() -> Path:
    return _corpus_dir() / ".eda_faiss_index"


def _line_at_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def _split_windows(text: str, max_chars: int, overlap: int) -> list[str]:
    if len(text) <= max_chars:
        return [text] if text.strip() else []
    step = max(256, max_chars - overlap)
    out: list[str] = []
    i = 0
    while i < len(text):
        piece = text[i : i + max_chars].strip()
        if piece:
            out.append(piece)
        i += step
        if i >= len(text):
            break
    return out


def chunk_markdown(md_path: Path, max_chars: int = _MAX_CHUNK, overlap: int = _OVERLAP) -> list[dict[str, Any]]:
    raw = md_path.read_text(encoding="utf-8")
    matches = list(HEADING_PATTERN.finditer(raw))
    records: list[dict[str, Any]] = []

    def push_section(section_text: str, start_line: int) -> None:
        section_text = section_text.strip()
        if not section_text:
            return
        first_line = section_text.split("\n", 1)[0].strip()
        for wi, piece in enumerate(_split_windows(section_text, max_chars, overlap)):
            rec_id = len(records)
            heading = first_line[:300]
            if wi > 0:
                heading = f"{heading} (continued {wi + 1})"
            records.append(
                {
                    "chunk_id": rec_id,
                    "heading": heading,
                    "start_line": start_line,
                    "text": piece,
                }
            )

    if matches and matches[0].start() > 0:
        pre = raw[: matches[0].start()].strip()
        if pre:
            push_section(pre, 1)

    if not matches:
        push_section(raw, 1)
        return records

    for j, m in enumerate(matches):
        sec_start = m.start()
        sec_end = matches[j + 1].start() if j + 1 < len(matches) else len(raw)
        section_text = raw[sec_start:sec_end].strip("\n").strip()
        start_line = _line_at_offset(raw, sec_start)
        push_section(section_text, start_line)

    # Re-number chunk_ids sequentially
    for i, rec in enumerate(records):
        rec["chunk_id"] = i
    return records


@dataclass
class IndexStore:
    dimension: int
    model_name: str
    source_path: Path
    chunks: list[dict[str, Any]]
    index: faiss.IndexFlatIP


def _encode_batch(model: SentenceTransformer, texts: list[str], batch_size: int = 32) -> np.ndarray:
    embs = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float32)
    return embs


def _validate_cache(meta_path: Path, cache_dir: Path, src: Path, model_name: str) -> bool:
    if not meta_path.is_file() or not (cache_dir / "index.faiss").is_file():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    stat = src.stat()
    return (
        meta.get("model_name") == model_name
        and meta.get("source_path") == str(src.resolve())
        and meta.get("source_mtime") == stat.st_mtime
        and meta.get("source_size") == stat.st_size
    )


def build_or_load() -> IndexStore:
    corpus = _corpus_dir()
    src = _source_path()
    if not src.is_file():
        raise FileNotFoundError(f"EDA corpus markdown not found: {src}")

    model_name = os.environ.get("EDA_EMBED_MODEL", _DEFAULT_MODEL).strip() or _DEFAULT_MODEL
    cdir = _cache_dir()
    meta_path = cdir / "meta.json"

    if _validate_cache(meta_path, cdir, src, model_name):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        chunks_path = cdir / "chunks.jsonl"
        chunks: list[dict[str, Any]] = []
        with chunks_path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    chunks.append(json.loads(line))
        chunks.sort(key=lambda x: int(x["chunk_id"]))
        index = faiss.read_index(str(cdir / "index.faiss"))
        dim = meta.get("dimension", index.d)
        _log(f"[eda-mcp] Loaded FAISS cache: {len(chunks)} chunks, dim={dim}")
        return IndexStore(dim, model_name, src, chunks, index)

    cdir.mkdir(parents=True, exist_ok=True)
    _log("[eda-mcp] Building embeddings (first run may download the model)...")
    records = chunk_markdown(src)
    if not records:
        raise ValueError(f"No text chunks produced from {src}")

    model = SentenceTransformer(model_name)
    texts = [r["text"] for r in records]
    embs = _encode_batch(model, texts)
    dim = embs.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embs)

    faiss.write_index(index, str(cdir / "index.faiss"))

    chunks_path = cdir / "chunks.jsonl"
    with chunks_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    stat = src.stat()
    meta = {
        "model_name": model_name,
        "source_path": str(src.resolve()),
        "source_mtime": stat.st_mtime,
        "source_size": stat.st_size,
        "num_chunks": len(records),
        "dimension": dim,
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    _log(f"[eda-mcp] Built index with {len(records)} chunks, dim={dim}")
    return IndexStore(dim, model_name, src, records, index)


_STORE: IndexStore | None = None
_EMBED_MODEL: SentenceTransformer | None = None
_EMBED_MODEL_NAME: str | None = None


def _embed_model(store: IndexStore) -> SentenceTransformer:
    global _EMBED_MODEL, _EMBED_MODEL_NAME
    if _EMBED_MODEL is None or _EMBED_MODEL_NAME != store.model_name:
        _EMBED_MODEL = SentenceTransformer(store.model_name)
        _EMBED_MODEL_NAME = store.model_name
    return _EMBED_MODEL


def _store() -> IndexStore:
    global _STORE
    if _STORE is None:
        _STORE = build_or_load()
    return _STORE


mcp = FastMCP("eda-faiss")


@mcp.tool()
def eda_search(query: str, top_k: int = 8) -> str:
    """Semantic search over the parsed EDA book (Hands-On Exploratory Data Analysis with Python).

    Args:
        query: Natural-language question or keywords (English or other languages).
        top_k: Number of passages to return (default 8, max 20).
    """
    store = _store()
    k = max(1, min(int(top_k), 20))

    model = _embed_model(store)
    qv = model.encode(
        [query.strip()],
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float32)
    scores, ids = store.index.search(qv, k)

    results: list[dict[str, Any]] = []
    snippet_cap = 1500
    for score, cid in zip(scores[0], ids[0], strict=False):
        if cid < 0:
            continue
        ch = store.chunks[cid]
        text = ch["text"]
        snippet = text if len(text) <= snippet_cap else text[:snippet_cap] + "…"
        results.append(
            {
                "chunk_id": int(ch["chunk_id"]),
                "score": float(score),
                "heading": ch.get("heading", ""),
                "start_line": ch.get("start_line"),
                "snippet": snippet,
            }
        )
    return json.dumps({"hits": results, "query": query, "top_k": k}, ensure_ascii=False, indent=2)


@mcp.tool()
def eda_chunk(chunk_id: int) -> str:
    """Fetch the full markdown text for a chunk by id (from eda_search results).

    Args:
        chunk_id: Index returned by eda_search in the chunk_id field.
    """
    store = _store()
    if chunk_id < 0 or chunk_id >= len(store.chunks):
        return json.dumps({"error": f"invalid chunk_id {chunk_id}, valid 0..{len(store.chunks) - 1}"})
    ch = store.chunks[chunk_id]
    payload = {"chunk_id": ch["chunk_id"], "heading": ch.get("heading"), "start_line": ch.get("start_line"), "text": ch["text"]}
    return json.dumps(payload, ensure_ascii=False, indent=2)


@mcp.tool()
def eda_stats() -> str:
    """Summary of the loaded corpus: path, embedding model, and chunk counts."""
    store = _store()
    summary = {
        "corpus_dir": str(_corpus_dir()),
        "markdown_source": str(store.source_path),
        "exists": store.source_path.is_file(),
        "embedding_model": store.model_name,
        "embedding_dimension": store.dimension,
        "num_chunks": len(store.chunks),
        "faiss_vectors": store.index.ntotal,
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


def main() -> None:
    _store()
    mcp.run()


if __name__ == "__main__":
    main()
