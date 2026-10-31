import json

import pytest

from src.streamstats.report import save_report


def test_save_report(tmp_path):

    """Проверяет создание JSON-отчёта."""

    output_file = tmp_path / "report.json"
    result = {
        "total_events": 3,
        "skipped_rows": 0,
        "level_counter": {
            "INFO": 2,
            "ERROR": 1
        }
    }
    save_report(result, output_file)
    assert output_file.exists()
    with output_file.open(encoding="utf-8") as file:
        report = json.load(file)
    assert report == result


def test_save_report_unicode(tmp_path):

    """Проверяет сохранение кириллицы."""

    output_file = tmp_path / "report.json"
    result = {"source": "сервер","message": "Ошибка подключения"}
    save_report(result, output_file)
    content = output_file.read_text(encoding="utf-8")
    assert "сервер" in content
    assert "Ошибка подключения" in content
    report = json.loads(content)
    assert report == result


def test_save_report_empty_data(tmp_path):

    """Проверяет сохранение пустого отчёта."""

    output_file = tmp_path / "empty_report.json"
    result = {}
    save_report(result, output_file)
    with output_file.open(encoding="utf-8") as file:
        report = json.load(file)
    assert report == {}


def test_save_report_invalid_path(tmp_path):

    """Проверяет ошибку при записи в несуществующую папку."""

    output_file = tmp_path / "missing" / "report.json"
    result = {"total_events": 1}
    with pytest.raises(OSError):
        save_report(result, output_file)
