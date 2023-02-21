
from httpx import Client
from rich.console import Console

from raycharles.utils import detect_parameters
from raycharles.payloads import PayloadGenerator


def spawn_shell(
    console: Console,
    session: Client,
    url: str,
    payload_func: PayloadGenerator
):
    """ Pseudo shell to facilitate commands execution """

    splitted_url = detect_parameters(url)

    while True:
        try:
            user_input = console.input("raycharles> ")
            payload    = payload_func(user_input)
            final_url  = ""

            for part in splitted_url:
                final_url += payload if part == "FUZZ" else part

            session.get(final_url)

            console.log("Request sent!")
        except KeyboardInterrupt:
            return
