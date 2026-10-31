import json
import subprocess
import sys


def test_cli_creates_report(tmp_path):
    input_file = tmp_path / "events.jsonl"

    events = [
        {
            "timestamp": "2026-10-28T09:00:00",
            "level": "INFO",
            "source": "api",
            "message": "Программа запущена"
        },
        {
            "timestamp": "2026-10-28T10:00:00",
            "level": "ERROR",
            "source": "database",
            "message": "Ошибка подключения"
        }
    ]

    with input_file.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")
    output_file = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "jsonl",
            "--output",
            str(output_file)
        ],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert result.returncode == 0
    with output_file.open(encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_events"] == 2
    assert report["level_counter"]["INFO"] == 1
    assert report["level_counter"]["ERROR"] == 1
    assert report["source_counter"]["api"] == 1
    assert report["source_counter"]["database"] == 1
    assert report["skipped_rows"] == 0
    assert report["first_timestamp"] == "2026-10-28T09:00:00"
    assert report["last_timestamp"] == "2026-10-28T10:00:00"
