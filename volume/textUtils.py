import re

def extractInt(text: str) -> int:
    try:
        return int(re.sub('\D', '', text))
    except ValueError as e:
        raise ValueError(f'Could not properly extract int from text: {text}') from e
    