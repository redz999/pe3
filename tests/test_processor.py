from pe3_generator.models import BomRow
from pe3_generator.processor import process_bom


def test_groups_and_ranges():
    rows = [
        BomRow("R1", "RES_10K", 1),
        BomRow("R2", "RES_10K", 1),
        BomRow("R3", "RES_10K", 1),
        BomRow("R5", "RES_10K", 1),
        BomRow("C1", "CAP_1UF", 1),
        BomRow("C2", "CAP_2UF", 1),
    ]

    lines = process_bom(rows)

    assert [line.position for line in lines] == ["C1", "C2", "R1-R3", "R5"]
    assert [line.name for line in lines] == ["CAP_1UF", "CAP_2UF", "RES_10K", "RES_10K"]
    assert [line.quantity for line in lines] == [1, 1, 3, 1]
