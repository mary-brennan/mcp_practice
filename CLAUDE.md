# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

`shellserver` is an early-stage MCP (Model Context Protocol) server. The project is currently a scaffold:
`README.md` and `server.py` are empty, and `src/shellserver/__init__.py` holds only a placeholder `main()`.
Nothing is committed yet (branch `master` has no commits). Treat existing files as starting points, not as
established conventions — there is no architecture to preserve yet.

It sits alongside sibling practice projects in `../mcp-client/` and `../mcp-servers/`, which are separate
repositories and not part of this one.

## Toolchain

Managed with **uv**; Python **3.14** is required (`requires-python = ">=3.14"`, pinned in `.python-version`).
Dependencies are `mcp[cli]`, which supplies both the MCP SDK and the `mcp` CLI, and `fastapi`.

```bash
uv sync                      # create/refresh .venv from uv.lock
uv add <package>             # add a dependency (updates pyproject.toml + uv.lock)
uv run shellserver           # run the console-script entry point (shellserver:main)
uv run mcp dev server.py     # run a server with the MCP Inspector for interactive testing
uv run mcp run server.py     # run a server directly over stdio
```

No test runner, linter, or formatter is configured yet. Adding one means `uv add --dev <tool>` plus the
matching config in `pyproject.toml`; until then there is no `uv run pytest` to invoke.

## Layout and packaging

Build backend is `uv_build` with the default src layout, so **only `src/shellserver/` is packaged**.
`pyproject.toml` declares the entry point `shellserver = "shellserver:main"`, meaning `main` must remain
importable from `src/shellserver/__init__.py`.

`server.py` at the repo root is outside the package. It is the conventional location for a `FastMCP`
instance that the `mcp` CLI loads by file path, but it is not importable as part of the installed
distribution. Code intended to ship (tools, resources, shell-execution logic) belongs under
`src/shellserver/`, with `server.py` kept as a thin entry point that imports from it.

## Code style

You are an expert in Python, FastAPI, and scalable API development.

Key principles:

- Write concise, technical responses with accurate Python examples.
- Use functional, declarative programming; avoid classes where possible.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g. `is_active`, `has_permission`).
