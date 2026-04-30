from dataclasses import dataclass


@dataclass(frozen=True)
class BomRow:
    designator: str
    part_number: str
    quantity: int


@dataclass(frozen=True)
class ElementLine:
    position: str
    name: str
    quantity: int
    note: str = ""
