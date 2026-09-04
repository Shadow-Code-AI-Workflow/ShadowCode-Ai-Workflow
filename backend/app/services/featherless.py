import os

import httpx
from dotenv import load_dotenv

load_dotenv()

FEATHERLESS_API_URL = "https://api.featherless.ai/v1/chat/completions"

FEATHERLESS_MODEL = os.getenv(
    "FEATHERLESS_MODEL",
    "Qwen/Qwen3-30B-A3B-Instruct-2507",
)


class FeatherlessService:
    def __init__(self):
        self.api_key = os.getenv("FEATHERLESS_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "FEATHERLESS_API_KEY is not configured"
            )

    async def chat(
        self,
        message: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        payload = {
            "model": FEATHERLESS_MODEL,
            "messages": messages,
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                FEATHERLESS_API_URL,
                headers=headers,
                json=payload,
            )

        if response.status_code >= 400:
            raise RuntimeError(
                f"Featherless API error "
                f"{response.status_code}: {response.text}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]