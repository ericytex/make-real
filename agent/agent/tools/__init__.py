from typing import Any, Callable, Dict, List, Optional


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        schema: Dict[str, Any],
        runner: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> None:
        self.name = name
        self.description = description
        self.schema = schema
        self.runner = runner

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return self.runner(args)


def get_all_tools() -> Dict[str, Tool]:
    # Lazy imports to avoid circulars
    from .shell import get_tools as shell_tools
    from .fs import get_tools as fs_tools
    from .web import get_tools as web_tools

    tools: Dict[str, Tool] = {}
    tools.update(shell_tools())
    tools.update(fs_tools())
    tools.update(web_tools())
    return tools


def get_tools(selected: Optional[List[str]] = None) -> Dict[str, Tool]:
    tools = get_all_tools()
    if not selected:
        return tools
    return {name: tool for name, tool in tools.items() if name in selected}
