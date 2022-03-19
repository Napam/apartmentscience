import json
from typing import Any, Union, Iterable
from dataclasses import dataclass
from pprint import pprint

JsonValue = str | float | bool | dict | list
FinnFilterDict = dict[str, Union[JsonValue, "FinnFilterDict"]]


@dataclass
class Filter:
    label: str
    queryParam: str


@dataclass
class FinnFilter:
    display_name: str
    name: str
    value: str
    hits: int
    filter_items: list["FinnFilter"]
    selected: bool

    def getFilter(self) -> dict:
        return Filter(self.display_name, self.value)


def loadFilterItems() -> list[FinnFilterDict]:
    with open("testfiters.json", "r") as f:
        return json.load(f)


def filterGenerator(filters: list[FinnFilterDict], maxDepth: float = float("inf")):
    mapFilterItems = lambda filters: (FinnFilter(**f) for f in filters)

    def _filterGenerator(filters: Iterable[FinnFilter], currDepth: int = 0):
        for f in filters:
            if (len(f.filter_items) == 0) or (currDepth == maxDepth):  # At bottom
                yield f.getFilter()
            else:
                yield from _filterGenerator(mapFilterItems(f.filter_items), currDepth + 1)

    yield from _filterGenerator(mapFilterItems(filters))


filteritems = loadFilterItems()
pprint(list(filterGenerator(filteritems, 1)))
