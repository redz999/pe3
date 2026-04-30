from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .bom_reader import BomValidationError, read_bom
from .processor import process_bom


def _write_csv(out_path: Path, lines: list) -> None:
    import csv

    with out_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow(["Поз. обозначение", "Наименование", "Кол.", "Примечание"])
        for line in lines:
            writer.writerow([line.position, line.name, line.quantity, line.note])


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PE3 Generator")
        self.geometry("760x220")
        self.resizable(False, False)

        self.bom_path = tk.StringVar()
        self.out_path = tk.StringVar()
        self.status = tk.StringVar(value="Выберите BOM и путь сохранения CSV")

        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="BOM (.xlsx):").grid(row=0, column=0, sticky="w")
        ttk.Entry(root, textvariable=self.bom_path, width=72).grid(row=1, column=0, sticky="we")
        ttk.Button(root, text="Выбрать", command=self._pick_bom).grid(row=1, column=1, padx=(8, 0))

        ttk.Label(root, text="Выходной CSV:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(root, textvariable=self.out_path, width=72).grid(row=3, column=0, sticky="we")
        ttk.Button(root, text="Сохранить как", command=self._pick_out).grid(row=3, column=1, padx=(8, 0))

        ttk.Button(root, text="Сгенерировать", command=self._generate).grid(row=4, column=0, sticky="w", pady=(14, 0))
        ttk.Label(root, textvariable=self.status).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _pick_bom(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if path:
            self.bom_path.set(path)
            if not self.out_path.get():
                self.out_path.set(str(Path(path).with_suffix(".csv")))

    def _pick_out(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            self.out_path.set(path)

    def _generate(self) -> None:
        bom = self.bom_path.get().strip()
        out = self.out_path.get().strip()
        if not bom or not out:
            messagebox.showerror("Ошибка", "Нужно выбрать BOM и выходной CSV")
            return

        try:
            rows = read_bom(bom)
            lines = process_bom(rows)
            out_path = Path(out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            _write_csv(out_path, lines)
            self.status.set(f"Готово. Сформировано строк: {len(lines)}")
            messagebox.showinfo("Успех", f"Файл сохранён: {out_path}")
        except BomValidationError as exc:
            messagebox.showerror("Ошибка BOM", str(exc))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Ошибка", f"Не удалось сформировать файл: {exc}")


def main() -> int:
    app = App()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
