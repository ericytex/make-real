import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .model import OpenAIChatModel
from .tools import get_tools, Tool


SYSTEM_PROMPT = (
    "You are a helpful software agent. "
    "You can think step by step and call tools to achieve the user's goal. "
    "When you decide to call a tool, respond ONLY with a JSON object of the form "
    "{\"tool\": string, \"args\": object}. "
    "Otherwise, write a concise natural language reply for the user. "
)


@dataclass
class AgentConfig:
    max_steps: int = 20
    selected_tools: Optional[List[str]] = None
    temperature: float = 0.2
    max_output_tokens: int = 800


class Agent:
    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        self.config = config or AgentConfig()
        self.model = OpenAIChatModel()
        self.tools: Dict[str, Tool] = get_tools(self.config.selected_tools)

    def run(self, user_goal: str) -> str:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_goal},
        ]

        for step in range(self.config.max_steps):
            reply = self.model.complete_chat(
                messages, self.config.temperature, self.config.max_output_tokens
            )

            tool_call = self._maybe_parse_tool_call(reply)
            if tool_call is None:
                return reply

            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("args", {})

            if tool_name not in self.tools:
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(tool_call),
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {"ok": False, "error": f"Unknown tool: {tool_name}"}
                        ),
                    }
                )
                continue

            tool = self.tools[tool_name]
            result = tool.run(tool_args)

            messages.append({"role": "assistant", "content": json.dumps(tool_call)})
            messages.append({"role": "tool", "content": json.dumps(result)})
            time.sleep(0.1)

        return "Reached max steps without resolution. Please refine your request."

    @staticmethod
    def _maybe_parse_tool_call(text: str) -> Optional[Dict[str, Any]]:
        text = text.strip()
        if not (text.startswith("{") and text.endswith("}")):
            return None
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                return None
            if "tool" in data and "args" in data:
                return data
            return None
        except json.JSONDecodeError:
            return None
