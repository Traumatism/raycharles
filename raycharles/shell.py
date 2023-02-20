import httpx

from rich.console import Console

from raycharles.utils import detect_parameters
from raycharles.payloads import PayloadGenerator


def spawn_shell(
    console: Console, session: httpx.Client, url: str, payload_fnc: PayloadGenerator
):
    splitted_url = detect_parameters(url)

    while True:
        try:
            user_input = console.input("raycharles> ")
            payload = payload_fnc(user_input)

            final_url = ""

            for part in splitted_url:
                if part == "FUZZ":
                    final_url += payload
                else:
                    final_url += part

            session.get(final_url)
            console.log("Request sent!")
        except KeyboardInterrupt:
            return
