import json
from typing import Iterable, MutableMapping
from pygments import highlight, lexers, formatters
import datetime as dt

isoNow = lambda: dt.datetime.now().isoformat()


def jprint(data: dict, file: str | None = None, indent: int = 4) -> str | None:
    dump = json.dumps(data, indent=indent)
    if file:
        with open(file, "w+") as f:
            f.write(dump)
    else:
        print(highlight(dump, lexers.JsonLexer(), formatters.TerminalFormatter(bg="dark")))


def _flatten_dict_gen(d: MutableMapping, parentKey: str, sep: str):
    for k, v in d.items():
        newKey = parentKey + sep + k if parentKey else k
        if isinstance(v, MutableMapping):
            yield from flattenDict(v, newKey, sep=sep).items()
        else:
            yield newKey, v


def flattenDict(d: MutableMapping, parent_key: str = "", sep: str = "_"):
    return dict(_flatten_dict_gen(d, parent_key, sep))


if __name__ == "__main__":
    from pprint import pprint
