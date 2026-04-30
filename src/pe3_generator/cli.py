from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .bom_reader import BomValidationError, read_bom
from .processor import process_bom


def main() -> int:
    parser = argparse.ArgumentParser(description="Генератор строк перечня элементов")
    parser.add_argument("bom", help="Путь к BOM-файлу .xlsx")
    parser.add_argument("--out", required=True, help="Путь к CSV-выгрузке строк ПЭ3")
    args = parser.parse_args()

    try:
        bom_rows = read_bom(args.bom)
        lines = process_bom(bom_rows)
    except BomValidationError as exc:
        print(str(exc))
        return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow(["Поз. обозначение", "Наименование", "Кол.", "Примечание"])
        for line in lines:
            writer.writerow([line.position, line.name, line.quantity, line.note])

    print(f"Сформировано строк: {len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
