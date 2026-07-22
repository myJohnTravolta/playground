import os
import requests

from dotenv import load_dotenv

load_dotenv()

#MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
MODEL = "cohere/north-mini-code:free"

def post_chat(
    messages: list[dict],
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> str:
    body: dict = {"model": MODEL, "messages": messages}
    if temperature is not None:
        body["temperature"] = temperature
    if max_tokens is not None:
        body["max_tokens"] = max_tokens

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        },
        json=body,
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(f"API error: {data['error']}")
    return data["choices"][0]["message"]["content"]
