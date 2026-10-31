import json


def save_report(path,report) -> None:

    """Функция сохраняет результаты анализа в JSON-файл.

       Использует кодировку UTF-8 и форматирует JSON."""

    with open(report,"w", encoding="utf-8") as file:
        json.dump(path, file, ensure_ascii=False, indent=4)
