# Сборка PE3 Generator под Windows

## Требования
- Windows 10/11
- Python 3.10+

## Шаги сборки EXE

Откройте PowerShell в корне проекта и выполните:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
./packaging/build_windows.ps1
```

После сборки исполняемый файл будет здесь:

- `dist/PE3Generator.exe`

## Запуск без сборки

```powershell
python -m pip install -e .
pe3-gui
```

Откроется графическое окно:
1. Выбрать BOM `.xlsx`
2. Выбрать путь сохранения `.csv`
3. Нажать «Сгенерировать»
