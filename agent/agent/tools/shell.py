import subprocess
from typing import Dict, Any

from . import Tool


def run_command(args: Dict[str, Any]) -> Dict[str, Any]:
    command: str = args.get("command", "")
    timeout: int = int(args.get("timeout", 120))
    if not command:
        return {"ok": False, "error": "Missing 'command'"}
    try:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timeout"}


def get_tools() -> Dict[str, Tool]:
    return {
        "shell.run": Tool(
            name="shell.run",
            description="Run a shell command non-interactively and return stdout, stderr, and return code.",
            schema={
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "timeout": {"type": "integer", "minimum": 1, "default": 120},
                },
                "required": ["command"],
            },
            runner=run_command,
        )
    }
