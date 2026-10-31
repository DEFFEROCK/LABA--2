import csv
import json
from pathlib import Path
from src.streamstats.models import parse_event
from src.streamstats.errors import InvalidEventError, InvalidFormatError



def check_format(path, skip_invalid=False, skipped_stats=None):

    """"Проверяет формат файла,
    если формат не .csv или не .jsonl,
    то выведет ошибку."""

    format_file = Path(path).suffix.lower()
    if format_file == ".csv":
        return csv_parser(path, skip_invalid, skipped_stats)
    elif format_file == ".jsonl":
        return jsonl_parser(path, skip_invalid, skipped_stats)
    else:
        raise InvalidFormatError(f"Неверный формат файла: {format_file}")




def csv_parser(path, skip_invalid=False,skipped_stats=None):

    """Парсит csv файл, возвращая список из событий"""

    if skipped_stats is None:
        skipped_stats = {"count": 0}
    with open(path, encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for line_number, row in enumerate(reader, start=2):
            try:
                event = parse_event(row)
            except InvalidEventError as error:
                message = f"CSV, строка {line_number}: {error}"
                if skip_invalid:
                    print(f"Предупреждение: {message}")
                    skipped_stats["count"] += 1
                    continue
                raise InvalidEventError(message) from error
            yield event


def jsonl_parser(path, skip_invalid=False,skipped_stats=None):

    """Парсит jsonl файл, возвращая список из событий"""

    if skipped_stats is None:
        skipped_stats = {"count": 0}
    with open(path, encoding="utf-8-sig") as jsonl_file:
        for line_number, line in enumerate(jsonl_file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise InvalidEventError("ожидался JSON-объект")
                event = parse_event(row)
            except (json.JSONDecodeError, InvalidEventError) as error:
                message = f"JSONL, строка {line_number}: {error}"
                if skip_invalid:
                    print(f"Предупреждение: {message}")
                    skipped_stats["count"] += 1
                    continue
                raise InvalidEventError(message) from error
            yield event


def execute(path, skip_invalid=False,skipped_stats=None):

    """"Проверяет формат исходного файла, если файл .csv или .jsonl,
    то будет парсить этот файл, иначе ошибка"""

    return check_format(path, skip_invalid, skipped_stats)


