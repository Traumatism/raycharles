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
