import os
import requests

from dotenv import load_dotenv

load_dotenv()

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def post_chat(messages: list[dict]) -> str:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        },
        json={
            "model": MODEL,
            "messages": messages,
        },
    )
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(f"API error: {data['error']}")
    return data["choices"][0]["message"]["content"]
