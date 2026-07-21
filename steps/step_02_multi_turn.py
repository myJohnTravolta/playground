# interactive chat loop; conversation history is kept in memory and resent each turn

import requests

from .client import post_chat


def run():
    messages = []

    print("Chat started. Type 'quit' to exit.\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "quit":
                break

            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                assistant_message = post_chat(messages)
            except requests.RequestException as e:
                print(f"API error: {e}\n")
                messages.pop()
                continue

            messages.append({"role": "assistant", "content": assistant_message})
            print(f"Assistant: {assistant_message}\n")

    except KeyboardInterrupt:
        print("\nGoodbye.")
