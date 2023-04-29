from re import sub


def convertToKebabCase(s):
    return '-'.join(
        sub(r"(\s|_|-)+", " ",
            sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                lambda mo: ' ' + mo.group(0).lower(), s)).split()).replace(".", "")


def sanitizeString(string: str) -> str:
    return string.strip()
