import json
from types import FunctionType
from typing import Any, Callable, Iterable, MutableMapping
from pygments import highlight, lexers, formatters
import datetime as dt
import config
import os
import tqdm

isoNow = lambda: dt.datetime.now().isoformat()


def jprint(data: dict, file: str | None = None, indent: int = 4) -> str | None:
    dump = json.dumps(data, indent=indent)
    if file:
        with open(file, "w+") as f:
            f.write(dump)
    else:
        print(highlight(dump, lexers.JsonLexer(), formatters.TerminalFormatter(bg="dark")))


def _flatten_dict_gen(d: MutableMapping, parentKey: str, sep: str, mapper: FunctionType):
    for k, v in d.items():
        newKey = parentKey + sep + k if parentKey else k
        if isinstance(v, MutableMapping):
            yield from flattenDict(v, newKey, sep=sep).items()
        else:
            yield newKey, mapper(v)


def flattenDict(
    d: MutableMapping, parent_key: str = "", sep: str = "_", mapper: FunctionType | None = None
):
    if mapper is None:
        mapper = lambda x: x

    return dict(_flatten_dict_gen(d, parent_key, sep, mapper))


def docs(flatten: bool = True, progress_bar: bool = False):
    for file in tqdm.tqdm(os.listdir(config.TMP_DIR), disable=not progress_bar):
        with open(os.path.join(config.TMP_DIR, file), "r") as f:
            try:
                docs: list[dict] = json.load(f)["docs"]
            except KeyError as e:
                print("Error loading a json from tmp dir: " + file)
                raise e
    
            for doc in docs:
                yield flattenDict(doc) if flatten else doc


def findFirst(x: Iterable[Any], predicate: Callable[[Any], bool]) -> Any | None:
    return next((item for item in x if predicate(item)), None)


if __name__ == "__main__":
    from pprint import pprint
