from __future__ import annotations

from collections import defaultdict

from .models import BomRow, ElementLine
from .parser import natural_key, parse_designator


def _to_range(designators: list[str]) -> str:
    if len(designators) == 1:
        return designators[0]
    start = parse_designator(designators[0])
    end = parse_designator(designators[-1])
    return f"{start.prefix}{start.number}-{end.prefix}{end.number}"


def _build_lines_for_group(rows: list[BomRow]) -> list[ElementLine]:
    rows_sorted = sorted(rows, key=lambda row: natural_key(row.designator))
    chunks: list[list[BomRow]] = []
    current: list[BomRow] = []

    for row in rows_sorted:
        if not current:
            current = [row]
            continue

        prev = current[-1]
        prev_key = natural_key(prev.designator)
        cur_key = natural_key(row.designator)

        contiguous = prev_key[0] == cur_key[0] and prev_key[1] + 1 == cur_key[1]
        same_part = prev.part_number == row.part_number

        if contiguous and same_part:
            current.append(row)
        else:
            chunks.append(current)
            current = [row]

    if current:
        chunks.append(current)

    lines: list[ElementLine] = []
    for chunk in chunks:
        lines.append(
            ElementLine(
                position=_to_range([row.designator for row in chunk]),
                name=chunk[0].part_number,
                quantity=sum(row.quantity for row in chunk),
                note="",
            )
        )
    return lines


def process_bom(rows: list[BomRow]) -> list[ElementLine]:
    groups: dict[str, list[BomRow]] = defaultdict(list)
    for row in rows:
        prefix, _ = natural_key(row.designator)
        groups[prefix].append(row)

    result: list[ElementLine] = []
    for prefix in sorted(groups.keys()):
        result.extend(_build_lines_for_group(groups[prefix]))
    return result
