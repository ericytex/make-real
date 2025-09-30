import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


@dataclass
class OpenAISettings:
    api_key: Optional[str]
    model: str
    base_url: Optional[str]


def load_openai_settings() -> OpenAISettings:
    return OpenAISettings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_openai_client() -> OpenAI:
    settings = load_openai_settings()
    client = OpenAI(
        api_key=settings.api_key if settings.api_key else None,
        base_url=settings.base_url if settings.base_url else None,
    )
    return client
