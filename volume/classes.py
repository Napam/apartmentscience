from dataclasses import dataclass
from typing import Any


@dataclass
class Paging:
    param: str
    current: float
    last: float


@dataclass
class FinnResponse:
    docs: list[dict[str, str | float]]
    filters: list[dict[str, Any]]
    metadata: list[dict[str, Any]]
    mapUrl: str
    isOdin: bool
    pageMetadata: list[dict[str, Any]]
