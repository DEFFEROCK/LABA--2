import json
import pytest

from src.streamstats.parsers import csv_parser, jsonl_parser
from src.streamstats.errors import InvalidEventError


def test_csv_parser(tmp_path):
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
    file = tmp_path / "events.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "wrong,INFO,api,Started\n",
        encoding="utf-8"
    )

    with pytest.raises(InvalidEventError):
        list(csv_parser(file))


def test_jsonl_invalid_row(tmp_path):
    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp": invalid json}\n',
        encoding="utf-8"
    )

    with pytest.raises(InvalidEventError):
        list(jsonl_parser(file))


def test_csv_skip_invalid(tmp_path):
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
