from datetime import datetime

import pytest

from src.streamstats.errors import InvalidEventError
from src.streamstats.models import Event, parse_event


def test_event_creation():

    """Проверяет создание объекта Event и корректность сохранения его атрибутов."""

    event = Event(
        timestamp=datetime.fromisoformat("2026-10-28T09:00:00"),
        level="INFO",
        source="api",
        message="Программа запущена",
    )

    assert event.level == "INFO"
    assert event.source == "api"
    assert event.message == "Программа запущена"


def test_parse_event_invalid_timestamp():

    """Проверяет, что при некорректной временной метке функция parse_event вызывает InvalidEventError."""


    row = {
        "timestamp": "invalid-date",
        "level": "INFO",
        "source": "api",
        "message": "test",
    }

    with pytest.raises(InvalidEventError):
        parse_event(row)


def test_parse_event_invalid_level():

    """Проверяет, что при недопустимом уровне события функция parse_event вызывает InvalidEventError."""

    row = {
        "timestamp": "2026-10-28T09:00:00",
        "level": "UNKNOWN",
        "source": "api",
        "message": "test",
    }

    with pytest.raises(InvalidEventError):
        parse_event(row)


def test_parse_event_empty_source():

    """Проверяет, что при пустом или состоящем из пробелов источнике функция parse_event вызывает InvalidEventError."""

    row = {
        "timestamp": "2026-10-28T09:00:00",
        "level": "INFO",
        "source": "   ",
        "message": "test",
    }

    with pytest.raises(InvalidEventError):
        parse_event(row)


def test_parse_event_valid_data():

    """Проверяет корректное создание объекта Event из словаря с валидными данными."""

    row = {
        "timestamp": "2026-10-28T09:00:00",
        "level": "ERROR",
        "source": "database",
        "message": "Ошибка подключения",
    }

    event = parse_event(row)

    assert event.timestamp == datetime.fromisoformat(
        "2026-10-28T09:00:00"
    )
    assert event.level == "ERROR"
    assert event.source == "database"
    assert event.message == "Ошибка подключения"