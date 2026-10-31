from dataclasses import dataclass
from datetime import datetime

from src.streamstats.errors import InvalidEventError, InvalidTimeMarkError


@dataclass
class Event:
    timestamp: datetime
    level: str
    source: str
    message: str
def parse_event(row: dict) -> Event:

    """Функция преобразует строку с данными события в объект Event.

    Проверяет корректность временной отметки, допустимость уровня события (DEBUG, INFO, WARNING, ERROR, CRITICAL) и наличие источника.

    Если данные некорректны, вызывает исключение InvalidEventError.

    При успешной проверке возвращает объект Event с полученными данными."""

    try:
        timestamp = datetime.fromisoformat(row["timestamp"])
    except (ValueError, TypeError) as error:
        raise InvalidTimeMarkError(
            f"Некорректная дата: {row.get('timestamp')}"
        ) from error
    Levels = {"DEBUG",
              "INFO",
              "WARNING",
              "ERROR",
              "CRITICAL"
    }
    if row["level"] not in Levels:
        raise InvalidEventError("Недопустимый уровень события")
    if not row["source"].strip():
        raise InvalidEventError("Source не может быть пустым")
    return Event(timestamp,
                 row["level"],
                 row["source"],
                 row["message"]
    )
