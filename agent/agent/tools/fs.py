import os
from typing import Dict, Any

from . import Tool


def read_file(args: Dict[str, Any]) -> Dict[str, Any]:
    path: str = args.get("path", "")
    if not path:
        return {"ok": False, "error": "Missing 'path'"}
    if not os.path.exists(path):
        return {"ok": False, "error": "File not found"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {"ok": True, "content": f.read()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def write_file(args: Dict[str, Any]) -> Dict[str, Any]:
    path: str = args.get("path", "")
    content: str = args.get("content", "")
    if not path:
        return {"ok": False, "error": "Missing 'path'"}
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_dir(args: Dict[str, Any]) -> Dict[str, Any]:
    path: str = args.get("path", ".")
    try:
        entries = os.listdir(path)
        return {"ok": True, "entries": entries}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_tools() -> Dict[str, Tool]:
    return {
        "fs.read_file": Tool(
            name="fs.read_file",
            description="Read a text file and return its contents.",
            schema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
            runner=read_file,
        ),
        "fs.write_file": Tool(
            name="fs.write_file",
            description="Write text content to a file, creating directories as needed.",
            schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
            runner=write_file,
        ),
        "fs.list_dir": Tool(
            name="fs.list_dir",
            description="List directory entries.",
            schema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
            runner=list_dir,
        ),
    }
