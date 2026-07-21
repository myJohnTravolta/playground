# single API request, prints the response, exits

from .client import post_chat


def run():
    reply = post_chat([{"role": "user", "content": "Hi"}])
    print(reply)
