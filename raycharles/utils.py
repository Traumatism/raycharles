import httpx
import time


def detect_parameters(url: str):
    """ Detect where are the injection entrypoints """

    target = [""]
    idx = 0

    for char in url:
        if char == "*":
            idx += 2
            target.append("FUZZ")
            target.append("")
        else:
            target[idx] += char

    return target[:-1] if target[-1] == "" else target


def detect_avg_ping(session: httpx.Client, url: str, requests: int = 15) -> float:
    """ Detect the average website response time for a better
    accuracy with blind injection detection """

    times = []

    for _ in range(requests):
        start_time = time.time()

        session.get(url)

        total_time = time.time() - start_time

        times.append(total_time)

    return sum(times) / len(times)
