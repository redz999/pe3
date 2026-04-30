# PE3 Generator

Прототип утилиты для формирования строк перечня элементов (ПЭ3) по BOM из Altium.

## Что уже реализовано

- Чтение BOM из `xlsx` (первый лист).
- Проверка обязательных колонок:
  - `Designator`
  - `Part Number`
  - `Quantity`
- Группировка по позиционным префиксам (`R`, `C`, `U` ...).
- Естественная сортировка (`R1`, `R2`, `R10`).
- Объединение последовательных обозначений с одинаковым `Part Number`
  в диапазоны (`R1-R13`).
- Экспорт промежуточного результата в CSV с колонками ПЭ3:
  - Поз. обозначение
  - Наименование
  - Кол.
  - Примечание
- Графическое окно для Windows (`pe3-gui`) и скрипт сборки `exe`.

## Быстрый запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pe3-generate ./input/bom.xlsx --out ./out/pe3.csv
```

## GUI запуск

```bash
pip install -e .
pe3-gui
```

## Сборка под Windows

Инструкция и скрипт:
- `packaging/README_WINDOWS.md`
- `packaging/build_windows.ps1`

Результат сборки: `dist/PE3Generator.exe`.

## Структура

- `src/pe3_generator/bom_reader.py` — чтение и валидация BOM.
- `src/pe3_generator/processor.py` — группировка, сортировка, схлопывание диапазонов.
- `src/pe3_generator/cli.py` — CLI-точка входа.
- `src/pe3_generator/gui.py` — desktop-окно для Windows.

## Дальше

Следующий этап: подключение Word-шаблона и генерация `DOCX`/`PDF`.
