# shellserver

A minimal MCP (Model Context Protocol) server that exposes a single tool, `terminal`, for running
shell commands on the host machine. Built with the Python `mcp` SDK (v2.x) and managed with `uv`.

The whole server is one file: [`server.py`](server.py).

## Requirements

- **Python 3.14** (pinned in `.python-version`)
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — installs Python and dependencies
- **Node.js / `npx`** — only for `mcp dev`, which launches the MCP Inspector

## Install

```bash
git clone <this repo>
cd shellserver
uv sync
```

`uv sync` creates `.venv` from `uv.lock` and installs `mcp[cli]` (the SDK plus the `mcp` CLI) and
`fastapi`. There is nothing to build — this project is not packaged, so `server.py` is run by path.

## Run

### Interactive testing with the MCP Inspector

```bash
uv run mcp dev server.py
```

Opens the Inspector in a browser, where you can list the tool, fill in its arguments, and see the
raw JSON-RPC traffic. This is the easiest way to try the server by hand.

### As a stdio server

```bash
uv run mcp run server.py   # via the mcp CLI
uv run python server.py    # equivalent, uses the __main__ block
```

Both speak MCP over stdin/stdout, so they will look like they are hanging — that is expected. This
is the form an MCP client launches.

## Connect a client

### Claude Desktop

```bash
uv run mcp install server.py
```

This writes an entry into `claude_desktop_config.json` (on Windows,
`%APPDATA%\Roaming\Claude\`). Restart Claude Desktop afterwards and `shellserver` will appear in
the tools list. Pass `--name` to register it under a different name.

### Claude Code

```bash
claude mcp add shellserver -- uv run --directory /absolute/path/to/shellserver mcp run server.py
```

### Any other client

Point it at the same command, using absolute paths:

```json
{
  "mcpServers": {
    "shellserver": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/shellserver", "mcp", "run", "server.py"]
    }
  }
}
```

## The `terminal` tool

Runs a command through the system shell (`cmd.exe` on Windows, `/bin/sh` elsewhere) and returns its
exit code, stdout and stderr as text.

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `command` | string | *(required)* | The command line to run, e.g. `ls -la` or `git status`. |
| `working_directory` | string | `"."` | Directory to run the command in, relative to where the server was started. |
| `timeout_seconds` | integer | `60` | Abort the command after this many seconds. |

Example result for `echo hello`:

```
exit code: 0

stdout:
hello
```

Failures are returned as text rather than raised, so the client sees the reason:

```
error: command timed out after 60s: sleep 300
error: working directory not found: /nope
```

## Security

The tool runs whatever it is given, with your user's privileges and no allowlist — including
destructive commands. That is fine for local experimentation, but do not expose this server over a
network transport or connect it to an untrusted client without adding restrictions first.
