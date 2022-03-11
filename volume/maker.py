import io
import os
import json
from types import NoneType

from attr import frozen
import utils
import pathlib
from pprint import pprint

TMP_DIR = pathlib.Path("data") / "apartmentscience" / "indexjsons"


def docs(flatten: bool = True):
    for file in os.listdir(TMP_DIR):
        with open(os.path.join(TMP_DIR, file), "r") as f:
            docs: list[dict] = json.load(f)["docs"]
            for doc in docs:
                yield utils.flattenDict(doc) if flatten else doc


def typeMapFromFlatDict():
    union: dict[str, set] = {}
    for doc in docs():
        for key, val in doc.items():
            union.setdefault(key, set())
            union[key].add(type(val))
    return union


def flatTypeMapToPythonClassString(typeMap: dict[str, set], name: str, tab: str = "    "):
    buffer = io.StringIO()
    buffer.write(f"class {name}:\n{tab}")

    def extractTypeString(type_):
        if type_ is NoneType:
            return "None"
        else:
            return type_.__name__

    for key, types in typeMap.items():
        buffer.write(f"{key}: ")
        buffer.write(f"{' | '.join(extractTypeString(t) for t in types)} = None")
        buffer.write(f"\n{tab}")
    print(buffer.getvalue())
    buffer.close()


if __name__ == "__main__":
    typemap = typeMapFromFlatDict()
    pprint(typemap)
    flatTypeMapToPythonClassString(typemap, "Baba")
