from dataclasses import dataclass

@dataclass
class Paging:
    param: str
    current: float
    last: float