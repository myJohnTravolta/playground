import os
import requests

from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
    },
    json={
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": [
            {"role": "user", "content": "Hi"}
        ],
    },
)

#print(response.json())
response.raise_for_status()

print(response.json()["choices"][0]["message"]["content"])
