import io
from types import NoneType

import utils
from pprint import pprint


def typeMapFromFlatDict():
    union: dict[str, set] = {}
    for doc in utils.docs():
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
