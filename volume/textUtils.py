import re

def extractNumber(text: str) -> str | None:
    return re.sub('\D', '', text) or None