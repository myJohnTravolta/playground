import shlex
import requests

from .client import post_chat

TIMES_RANGE = (1, 20)
TEMPERATURE_RANGE = (0.0, 2.0)
MAX_TOKENS_RANGE = (1, 300)


def _parse_input(raw: str) -> tuple[str, int, float, int]:
    parts = shlex.split(raw.strip())
    if len(parts) != 4:
        raise ValueError('Expected: "prompt" times temperature max_tokens')

    prompt = parts[0]
    times = int(parts[1])
    temperature = float(parts[2])
    max_tokens = int(parts[3])

    if not prompt:
        raise ValueError("prompt cannot be empty")
    if not (TIMES_RANGE[0] <= times <= TIMES_RANGE[1]):
        raise ValueError(f"times must be between {TIMES_RANGE[0]} and {TIMES_RANGE[1]}")
    if not (TEMPERATURE_RANGE[0] <= temperature <= TEMPERATURE_RANGE[1]):
        raise ValueError(f"temperature must be between {TEMPERATURE_RANGE[0]} and {TEMPERATURE_RANGE[1]}")
    if not (MAX_TOKENS_RANGE[0] <= max_tokens <= MAX_TOKENS_RANGE[1]):
        raise ValueError(f"max_tokens must be between {MAX_TOKENS_RANGE[0]} and {MAX_TOKENS_RANGE[1]}")

    return prompt, times, temperature, max_tokens


def run():
    print("Temperature experiment")
    print('Enter parameters ("prompt" times temperature max_tokens):')
    print('  prompt      — quoted string, e.g. "Why is the sky blue?"')
    print(f"  times       — [{TIMES_RANGE[0]}, {TIMES_RANGE[1]}]")
    print(f"  temperature — [{TEMPERATURE_RANGE[0]}, {TEMPERATURE_RANGE[1]}]")
    print(f"  max_tokens  — [{MAX_TOKENS_RANGE[0]}, {MAX_TOKENS_RANGE[1]}]")
    print()

    while True:
        try:
            raw = input("> ").strip()
            prompt, times, temperature, max_tokens = _parse_input(raw)
            break
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}. Try again.\n")

    print(f'\nPrompt: "{prompt}"')
    print(f"Parameters: times={times}  temperature={temperature}  max_tokens={max_tokens}\n")
    print("-" * 60)

    messages = [{"role": "user", "content": prompt}]

    for i in range(1, times + 1):
        try:
            reply = post_chat(messages, temperature=temperature, max_tokens=max_tokens)
        except requests.RequestException as e:
            print(f"<--Run {i:02d}: ERROR — {e}")
            continue

        print(f"<--Run {i:02d}: {reply}")

    print("-" * 60)
