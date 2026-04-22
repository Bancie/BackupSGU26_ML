# BackupSGU26_ML

## MCP (Cursor)

Workspace MCP is defined in [`.cursor/mcp.json`](.cursor/mcp.json): **pandas-mcp** and **mcp-server-ds** (data exploration).

### One-time setup

1. Install [uv](https://github.com/astral-sh/uv) and Python **3.10+** (3.13 recommended if your default is 3.14; see below).

2. Clone both servers and install dependencies:

```bash
mkdir -p tools/mcp && cd tools/mcp
git clone https://github.com/marlonluo2018/pandas-mcp-server.git
git clone https://github.com/reading-plus-ai/mcp-server-data-exploration.git
cd pandas-mcp-server && uv sync && cd ..
cd mcp-server-data-exploration && uv python pin 3.13 && uv sync && cd ../..
```

`mcp-server-data-exploration` pins **Python 3.13** because its dependency stack (e.g. `pydantic-core` via older `mcp`) may not build on **Python 3.14** yet. `pandas-mcp-server` can use the default interpreter from `uv sync`.

3. Reload the Cursor window (**Developer: Reload Window**), then enable the MCP servers under **Settings → MCP**.

`tools/mcp/` is listed in `.gitignore`; only `.cursor/mcp.json` is meant to be committed so each machine runs its own clones and virtualenvs.
