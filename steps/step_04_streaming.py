import os

from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()

MODEL = "cohere/north-mini-code:free"
PROMPT = "Explain what Server-Sent Events are in 3 short sentences."


def run():
    print("Streaming demo")
    print(f"Model: {MODEL}")
    print(f"Prompt: {PROMPT}")
    print("-" * 60)

    full_response = ""

    with OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"]) as client:
        stream = client.chat.send(
            messages=[{"role": "user", "content": PROMPT}],
            model=MODEL,
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if isinstance(token, str):
                print(token, end="", flush=True)
                full_response += token

    print("\n" + "-" * 60)
    print(f"Full response ({len(full_response)} chars):")
    print(full_response)
