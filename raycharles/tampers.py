import base64


def default_tamper(cmd: str) -> str:
    return cmd


def replace_spaces_with_ifs(cmd: str) -> str:
    """ Replace space characters with ${IFS} """

    return cmd.replace(" ", "${IFS}")


def add_dollar_and_ats(cmd: str) -> str:
    """ Add a $@ after each letter """

    final = ""

    for char in cmd:
        final += char

        if char != " ":
            final += "$@"

    return final[:-2]


def encode_base64(cmd: str) -> str:
    """ Encode the command with base64 """
    return "bash<<<$(base64 -d<<<%s)" % base64.b64encode(cmd.encode()).decode()


def encapsulate_into_curly_braces(cmd: str) -> str:
    """ Encapsulate the command inside curly braces """
    return "{" + ",".join(cmd.split()) + "}"
