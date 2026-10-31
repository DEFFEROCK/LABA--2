from collections import Counter

from src.streamstats.parsers import execute


def analyze_events(paths, skip_invalid=False) -> dict:

    """Функция выполняет анализ одного или нескольких входных файлов.

    Подсчитывает общее количество событий, количество событий по уровням и источникам,
    определяет топ-5 источников ошибок уровня ERROR и CRITICAL,
    а также находит самую раннюю и самую позднюю временные отметки.

    При параметре skip_invalid=True пропускает некорректные строки и подсчитывает их количество.
    Возвращает словарь с результатами анализа."""

    total_events = 0
    skipped_stats = {"count": 0}
    level_counter = Counter()
    source_counter = Counter()
    errors_source_counter = Counter()
    first_timestamp = None
    last_timestamp = None
    for path in paths:
        result = execute(path, skip_invalid, skipped_stats)
        for event in result:
            total_events += 1
            level_counter[event.level] += 1
            source_counter[event.source] += 1
            if event.level in ("ERROR","CRITICAL"):
                errors_source_counter[event.source] += 1

            if first_timestamp is None or event.timestamp < first_timestamp:
                first_timestamp = event.timestamp

            if last_timestamp is None or event.timestamp > last_timestamp:
                last_timestamp = event.timestamp

    return {

        "total_events": total_events,
        "skipped_rows": skipped_stats["count"],
        "level_counter": dict(level_counter),
        "source_counter": dict(source_counter),

        "top_error_sources": [
            {"source": source, "count": count }
            for source, count in errors_source_counter.most_common(5)
        ],

        "first_timestamp": (
            first_timestamp.isoformat() if first_timestamp else None
        ),
        "last_timestamp": (
            last_timestamp.isoformat() if last_timestamp else None
                           ),

    }


