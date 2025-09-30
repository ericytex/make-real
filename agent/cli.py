import argparse
import json
import os
from typing import Optional

from agent import Agent, AgentConfig


def run(goal: str, tools: Optional[str]) -> None:
    selected_tools = tools.split(",") if tools else None
    agent = Agent(AgentConfig(selected_tools=selected_tools))
    result = agent.run(goal)
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Agent CLI")
    parser.add_argument("goal", type=str, help="User goal or instruction")
    parser.add_argument(
        "--tools",
        type=str,
        default=None,
        help="Comma-separated tool names to enable (default: all)",
    )
    args = parser.parse_args()
    run(args.goal, args.tools)


if __name__ == "__main__":
    main()
