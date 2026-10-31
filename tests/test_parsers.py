
import json

import pytest

from src.streamstats.errors import InvalidEventError, InvalidFormatError
from src.streamstats.parsers import check_format, csv_parser, jsonl_parser


def test_csv_parser(tmp_path):

    """Проверяет чтение CSV-файла и корректность извлечения данных о событии."""

    file = tmp_path / "events.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-28T09:00:00,INFO,api,Started\n",
        encoding="utf-8"
    )

    events = list(csv_parser(file))

    assert len(events) == 1
    assert events[0].level == "INFO"
    assert events[0].source == "api"


def test_jsonl_parser(tmp_path):

    """Проверяет чтение JSONL-файла и корректность извлечения данных о событии."""

    file = tmp_path / "events.jsonl"
    file.write_text(
        json.dumps({
            "timestamp": "2026-10-28T09:00:00",
            "level": "ERROR",
            "source": "database",
            "message": "Connection failed"
        }) + "\n",
        encoding="utf-8"
    )

    events = list(jsonl_parser(file))

    assert len(events) == 1
    assert events[0].level == "ERROR"
    assert events[0].source == "database"


def test_csv_invalid_row(tmp_path):

    """Проверяет, что CSV-парсер вызывает ошибку при обработке некорректной строки."""

    file = tmp_path / "events.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "wrong,INFO,api,Started\n",
        encoding="utf-8"
    )

    with pytest.raises(InvalidEventError):
        list(csv_parser(file))


def test_jsonl_invalid_row(tmp_path):

    """Проверяет, что JSONL-парсер вызывает ошибку при чтении некорректного JSON."""

    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp": invalid json}\n',
        encoding="utf-8"
    )

    with pytest.raises(InvalidEventError):
        list(jsonl_parser(file))


def test_csv_skip_invalid(tmp_path):

    """Проверяет пропуск некорректных строк в CSV-файле и подсчёт пропущенных записей."""

    file = tmp_path / "events.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "wrong,INFO,api,Invalid\n"
        "2026-10-28T09:00:00,INFO,api,Valid\n",
        encoding="utf-8"
    )

    skipped_stats = {"count": 0}

    events = list(csv_parser(
        file,
        skip_invalid=True,
        skipped_stats=skipped_stats
    ))

    assert len(events) == 1
    assert skipped_stats["count"] == 1


def test_jsonl_skip_invalid(tmp_path):

    """Проверяет пропуск некорректных JSONL-строк и подсчёт пропущенных записей."""

    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp": invalid json}\n'
        '{"timestamp":"2026-10-28T09:00:00",'
        '"level":"INFO","source":"api","message":"Valid"}\n',
        encoding="utf-8"
    )

    skipped_stats = {"count": 0}

    events = list(jsonl_parser(
        file,
        skip_invalid=True,
        skipped_stats=skipped_stats
    ))

    assert len(events) == 1
    assert skipped_stats["count"] == 1


def test_check_format_invalid(tmp_path):

    """Проверяет ошибку при передаче файла неподдерживаемого формата."""

    file = tmp_path / "events.txt"
    file.write_text("test", encoding="utf-8")

    with pytest.raises(InvalidFormatError):
        list(check_format(file))


def test_jsonl_empty_lines(tmp_path):

    """Проверяет пропуск пустых строк в JSONL-файле."""

    file = tmp_path / "events.jsonl"

    event = {
        "timestamp": "2026-10-28T09:00:00",
        "level": "INFO",
        "source": "api",
        "message": "Test"
    }

    file.write_text(
        "\n" + json.dumps(event) + "\n\n",
        encoding="utf-8"
    )

    events = list(jsonl_parser(file))

    assert len(events) == 1
    assert events[0].source == "api"


def test_jsonl_not_object(tmp_path):

    """Проверяет обработку JSON, который не является объектом."""

    file = tmp_path / "events.jsonl"
    file.write_text('"обычная строка"\n', encoding="utf-8")

    with pytest.raises(InvalidEventError, match="ожидался JSON-объект"):
        list(jsonl_parser(file))


def test_csv_skip_invalid_without_stats(tmp_path):

    """Проверяет создание счётчика пропущенных строк по умолчанию."""

    file = tmp_path / "events.csv"

    file.write_text(
        "timestamp,level,source,message\n"
        "wrong,INFO,api,Invalid\n",
        encoding="utf-8"
    )

    events = list(csv_parser(file, skip_invalid=True))

    assert events == []





def test_check_format_uppercase_csv(tmp_path):

    """Проверяет обработку расширения CSV в верхнем регистре."""

    file = tmp_path / "events.CSV"
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-28T09:00:00,INFO,api,test\n",
        encoding="utf-8"
    )

    events = list(check_format(file))

    assert len(events) == 1
    assert events[0].level == "INFO"


def test_check_format_uppercase_jsonl(tmp_path):

    """Проверяет обработку расширения JSONL в верхнем регистре."""

    file = tmp_path / "events.JSONL"
    file.write_text(
        '{"timestamp":"2026-10-28T09:00:00",'
        '"level":"INFO","source":"api","message":"test"}\n',
        encoding="utf-8"
    )

    events = list(check_format(file))

    assert len(events) == 1
    assert events[0].level == "INFO"


def test_check_format_unsupported_extension(tmp_path):

    """Проверяет ошибку при неподдерживаемом формате."""

    file = tmp_path / "events.txt"
    file.write_text("test", encoding="utf-8")

    with pytest.raises(InvalidFormatError):
        list(check_format(file))
