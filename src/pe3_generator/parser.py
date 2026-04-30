from __future__ import annotations

import re
from dataclasses import dataclass


DESIGNATOR_RE = re.compile(r"^\s*([A-Za-zА-Яа-я]+)\s*([0-9]+)\s*$")


@dataclass(frozen=True)
class ParsedDesignator:
    prefix: str
    number: int


def parse_designator(value: str) -> ParsedDesignator:
    match = DESIGNATOR_RE.match(value)
    if not match:
        raise ValueError(f"Некорректное позиционное обозначение: {value!r}")
    prefix, number_text = match.groups()
    return ParsedDesignator(prefix=prefix.upper(), number=int(number_text))


def natural_key(value: str) -> tuple[str, int]:
    parsed = parse_designator(value)
    return parsed.prefix, parsed.number
