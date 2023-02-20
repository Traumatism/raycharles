import base64


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


def encode_base64(cmd: str) -> str:
    return "bash<<<$(base64 -d<<<%s)" % base64.b64encode(cmd.encode()).decode()


def encapsulate_into_curly_braces(cmd: str) -> str:
    parts = cmd.split()
    return "{" + ",".join(parts) + "}"
