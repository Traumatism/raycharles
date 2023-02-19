def detect_parameters(url: str):
    target = [""]
    idx = 0

    for char in url:
        if char == "*":
            idx += 2
            target.append("FUZZ")
            target.append("")
        else:
            target[idx] += char

    return target[:-1] if target[-1] == "" else target
