from typing import List, Dict, Any, Optional

from .config import get_openai_client, load_openai_settings


class OpenAIChatModel:
    def __init__(self, model_name: Optional[str] = None):
        settings = load_openai_settings()
        self.model_name = model_name or settings.model
        self.client = get_openai_client()

    def complete_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_output_tokens: int = 800,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,  # type: ignore[arg-type]
            temperature=temperature,
            max_tokens=max_output_tokens,
        )
        return response.choices[0].message.content or ""
