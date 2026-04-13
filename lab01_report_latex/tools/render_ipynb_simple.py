#!/usr/bin/env python3
"""
Render a Jupyter .ipynb to a simple standalone HTML (no external deps).

Supports:
- markdown cells (very light: shows as-is, preserving line breaks)
- code cells (preformatted)
- outputs: stream text and image/png (base64)

Usage:
  python3 render_ipynb_simple.py input.ipynb output.html
"""

from __future__ import annotations

import base64
import html
import json
import sys
from pathlib import Path


def _h(s: str) -> str:
    return html.escape(s, quote=True)


def _join_source(src) -> str:
    if isinstance(src, list):
        return "".join(src)
    if isinstance(src, str):
        return src
    return str(src)


def render_notebook(ipynb_path: Path) -> str:
    nb = json.loads(ipynb_path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])

    parts: list[str] = []
    parts.append(
        """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Notebook Render</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; margin: 24px; }
    .cell { border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 14px; margin: 12px 0; }
    .md { white-space: pre-wrap; }
    pre { background: #0b1020; color: #e5e7eb; padding: 12px; border-radius: 10px; overflow-x: auto; }
    .out { margin-top: 10px; }
    .stream { background: #111827; color: #e5e7eb; padding: 10px; border-radius: 10px; white-space: pre-wrap; }
    img { max-width: 100%; height: auto; border: 1px solid #e5e7eb; border-radius: 10px; }
    .meta { color: #6b7280; font-size: 12px; margin-bottom: 6px; }
  </style>
</head>
<body>
"""
    )

    parts.append(f"<h1>{_h(ipynb_path.name)}</h1>\n")

    for idx, cell in enumerate(cells):
        ctype = cell.get("cell_type")
        src = _join_source(cell.get("source", ""))
        parts.append('<div class="cell">')
        parts.append(f'<div class="meta">cell {idx} · {ctype}</div>')

        if ctype == "markdown":
            parts.append(f'<div class="md">{_h(src)}</div>')
        elif ctype == "code":
            parts.append("<pre><code>")
            parts.append(_h(src))
            parts.append("</code></pre>")

            outputs = cell.get("outputs", []) or []
            if outputs:
                parts.append('<div class="out">')
                for out in outputs:
                    otype = out.get("output_type")
                    if otype == "stream":
                        text = _join_source(out.get("text", ""))
                        parts.append(f'<div class="stream">{_h(text)}</div>')
                    elif otype in ("display_data", "execute_result"):
                        data = out.get("data", {}) or {}
                        if "image/png" in data:
                            b64 = data["image/png"]
                            if isinstance(b64, list):
                                b64 = "".join(b64)
                            # validate base64 quickly
                            try:
                                base64.b64decode(b64[:64] + "==", validate=False)
                            except Exception:
                                pass
                            parts.append(f'<img alt="output" src="data:image/png;base64,{b64}"/>')
                        elif "text/plain" in data:
                            text = _join_source(data.get("text/plain", ""))
                            parts.append(f'<div class="stream">{_h(text)}</div>')
                    elif otype == "error":
                        ename = out.get("ename", "")
                        evalue = out.get("evalue", "")
                        tb = _join_source(out.get("traceback", ""))
                        parts.append(f'<div class="stream">{_h(ename)}: {_h(evalue)}\n{_h(tb)}</div>')
                parts.append("</div>")
        else:
            parts.append(f"<div>{_h(src)}</div>")

        parts.append("</div>")

    parts.append("</body></html>\n")
    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 render_ipynb_simple.py input.ipynb output.html", file=sys.stderr)
        return 2

    ipynb = Path(sys.argv[1]).expanduser().resolve()
    out = Path(sys.argv[2]).expanduser().resolve()

    html_text = render_notebook(ipynb)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

