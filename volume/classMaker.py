import io
from types import NoneType

import utils
from pprint import pprint


def typeMapFromFlatDict():
    union: dict[str, set] = {}
    for doc in utils.docs(progress_bar=True):
        for key, val in doc.items():
            union.setdefault(key, set())
            union[key].add(type(val))
    return union


def flatTypeMapToPythonClassString(
    typeMap: dict[str, set], name: str, indent: str = "    ", table: str | None = None
):
    def extractTypeString(type_):
        if type_ is NoneType:
            return "None"
        else:
            return type_.__name__

    def extractSATypeString(types: set):
        types = types - {NoneType}
        if (
            (str in types)
            or (list in types)
            or (tuple in types)
            or (set in types)
            or (dict in types)
        ):
            return "sa.UnicodeText"
        if float in types:
            return "sa.Float"
        if int in types:
            return "sa.Integer"

    buffer = io.StringIO()
    if table is not None:
        buffer.write(f"@mapper_registry.mapped\n")
        buffer.write(f"@dataclass\n")
    buffer.write(f"class {name}:\n{indent}")

    if table is not None:
        buffer.write("__table__ = sa.Table(\n")
        buffer.write(f'{indent*2}"{table}",\n')
        buffer.write(f"{indent*2}mapper_registry.metadata,\n")
        buffer.write(
            f'{indent*2}sa.Column("_id", sa.Integer, autoincrement=True, primary_key=True),\n'
        )
        buffer.write(f'{indent*2}sa.Column("_created", sa.DateTime, server_default=func.now()),\n')
        buffer.write(f'{indent*2}sa.Column("_last_updated", sa.DateTime, onupdate=func.now()),\n')
        buffer.write(f'{indent*2}sa.Column("_batch", sa.Integer),\n')
        for key, types in typeMap.items():
            buffer.write(f'{indent*2}sa.Column("{key}", {extractSATypeString(types)}),\n')
        buffer.write(f"{indent})\n")
        buffer.write(f"{indent}_id: int = field(init=False)\n")
        buffer.write(f"{indent}_last_updated: datetime.datetime = field(init=False)\n")
        buffer.write(f"{indent}_batch: int = None\n{indent}")

    for key, types in typeMap.items():
        buffer.write(f"{key}: ")
        buffer.write(f"{' | '.join(extractTypeString(t) for t in types)} = None")
        buffer.write(f"\n{indent}")
    print(buffer.getvalue())
    buffer.close()


if __name__ == "__main__":
    typemap = typeMapFromFlatDict()
    flatTypeMapToPythonClassString(typemap, "Doc", table="preview")
