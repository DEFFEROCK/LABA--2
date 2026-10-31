import json
import pytest

from src.streamstats.analysis import analyze_events
from src.streamstats.errors import InvalidEventError


def create_jsonl_file(path, events):

    """Создаёт JSONL-файл с тестовыми событиями."""

    with path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")


def test_analyze_events(tmp_path):

    """Проверяет общую статистику событий."""

    file = tmp_path / "events.jsonl"
    events = [
        {
            "timestamp": "2026-10-28T09:00:00",
            "level": "INFO",
            "source": "api",
            "message": "Started"
        },
        {
            "timestamp": "2026-10-28T09:05:00",
            "level": "ERROR",
            "source": "database",
            "message": "Failed"
        },
        {
            "timestamp": "2026-10-28T09:10:00",
            "level": "INFO",
            "source": "api",
            "message": "Finished"
        }
    ]
    create_jsonl_file(file, events)
    result = analyze_events([file])
    assert result["total_events"] == 3
    assert result["level_counter"]["INFO"] == 2
    assert result["level_counter"]["ERROR"] == 1
    assert result["source_counter"]["api"] == 2
    assert result["source_counter"]["database"] == 1
    assert result["skipped_rows"] == 0


def test_analyze_empty_file(tmp_path):

    """Проверяет анализ пустого файла."""

    file = tmp_path / "empty.jsonl"
    file.write_text("", encoding="utf-8")
    result = analyze_events([file])
    assert result["total_events"] == 0
    assert result["skipped_rows"] == 0
    assert result["level_counter"] == {}
    assert result["source_counter"] == {}
    assert result["top_error_sources"] == []
    assert result["first_timestamp"] is None
    assert result["last_timestamp"] is None


def test_analyze_multiple_files(tmp_path):

    """Проверяет объединение статистики нескольких файлов."""

    file1 = tmp_path / "first.jsonl"
    file2 = tmp_path / "second.jsonl"
    events1 = [
        {
            "timestamp": "2026-10-28T09:00:00",
            "level": "INFO",
            "source": "api",
            "message": "Started"
        }
    ]
    events2 = [
        {
            "timestamp": "2026-10-28T10:00:00",
            "level": "ERROR",
            "source": "database",
            "message": "Failed"
        }
    ]
    create_jsonl_file(file1, events1)
    create_jsonl_file(file2, events2)
    result = analyze_events([file1, file2])
    assert result["total_events"] == 2
    assert result["level_counter"]["INFO"] == 1
    assert result["level_counter"]["ERROR"] == 1
    assert result["source_counter"]["api"] == 1
    assert result["source_counter"]["database"] == 1


def test_analyze_timestamps(tmp_path):

    """Проверяет поиск первой и последней даты."""

    file = tmp_path / "events.jsonl"
    events = [
        {
            "timestamp": "2026-10-28T10:00:00",
            "level": "INFO",
            "source": "api",
            "message": "Second"
        },
        {
            "timestamp": "2026-10-28T08:00:00",
            "level": "INFO",
            "source": "api",
            "message": "First"
        },
        {
            "timestamp": "2026-10-28T12:00:00",
            "level": "ERROR",
            "source": "database",
            "message": "Last"
        }
    ]
    create_jsonl_file(file, events)
    result = analyze_events([file])
    assert result["first_timestamp"] == "2026-10-28T08:00:00"
    assert result["last_timestamp"] == "2026-10-28T12:00:00"


def test_analyze_top_error_sources(tmp_path):

    """Проверяет топ-5 источников ошибок."""

    file = tmp_path / "events.jsonl"
    events = []
    for source, count in [
        ("database", 5),
        ("api", 3),
        ("payment", 2),
        ("worker", 1),
        ("auth", 4),
        ("cache", 6)
    ]:
        for number in range(count):
            events.append({
                "timestamp": f"2026-10-28T09:{number:02d}:00",
                "level": "ERROR",
                "source": source,
                "message": "Error"
            })

    create_jsonl_file(file, events)
    result = analyze_events([file])
    assert len(result["top_error_sources"]) == 5
    assert result["top_error_sources"][0] == {
        "source": "cache",
        "count": 6
    }


def test_analyze_skip_invalid(tmp_path):

    """Проверяет пропуск некорректных строк."""

    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp": invalid json}\n'
        '{"timestamp":"2026-10-28T09:00:00",'
        '"level":"INFO","source":"api","message":"Valid"}\n',
        encoding="utf-8"
    )

    result = analyze_events([file], skip_invalid=True)

    assert result["total_events"] == 1
    assert result["skipped_rows"] == 1


def test_analyze_invalid_without_skip(tmp_path):

    """Проверяет ошибку при некорректной строке без skip_invalid."""

    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp": invalid json}\n',
        encoding="utf-8"
    )

    with pytest.raises(InvalidEventError):
        analyze_events([file])


def test_analyze_missing_file(tmp_path):

    """Проверяет обработку отсутствующего файла."""

    file = tmp_path / "missing.jsonl"
    with pytest.raises(OSError):
        analyze_events([file])
