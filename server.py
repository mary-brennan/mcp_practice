"""MCP server exposing a terminal tool and a read-only notes resource.

Run it with `uv run mcp dev server.py` (Inspector) or `uv run mcp run server.py` (stdio).
"""

import subprocess
from pathlib import Path

from mcp.server import MCPServer

DEFAULT_TIMEOUT_SECONDS = 60
MCP_README_PATH = Path.home() / "OneDrive" / "Desktop" / "mcpreadme.md"

mcp = MCPServer(
    "shellserver",
    instructions="Runs shell commands on the host machine via the `terminal` tool.",
)


def _format_result(returncode: int, stdout: str, stderr: str) -> str:
    """Render a completed command as a single readable block of text."""
    sections = [f"exit code: {returncode}"]
    if stdout.strip():
        sections.append(f"stdout:\n{stdout.rstrip()}")
    if stderr.strip():
        sections.append(f"stderr:\n{stderr.rstrip()}")
    if len(sections) == 1:
        sections.append("(no output)")
    return "\n\n".join(sections)


@mcp.tool(
    name="terminal",
    title="Terminal",
    description=(
        "Run a shell command on the host machine and return its exit code, "
        "stdout and stderr."
    ),
)
def terminal(
    command: str,
    working_directory: str = ".",
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> str:
    """Execute `command` in a shell and return its combined result.

    Args:
        command: The command line to run, e.g. `ls -la` or `git status`.
        working_directory: Directory to run the command in. Defaults to the
            directory the server was started from.
        timeout_seconds: Abort the command after this many seconds.
    """
    cwd = Path(working_directory).expanduser()
    if not cwd.is_dir():
        return f"error: working directory not found: {cwd}"

    try:
        completed = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return f"error: command timed out after {timeout_seconds}s: {command}"

    return _format_result(completed.returncode, completed.stdout, completed.stderr)


@mcp.resource(
    "file:///desktop/mcpreadme.md",
    name="mcpreadme",
    title="MCP README",
    description="The mcpreadme.md notes file from the Desktop directory.",
    mime_type="text/markdown",
)
def mcp_readme() -> str:
    """Return the current contents of Desktop/mcpreadme.md.

    The file is read on every request, so edits show up without restarting
    the server.
    """
    return MCP_README_PATH.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
