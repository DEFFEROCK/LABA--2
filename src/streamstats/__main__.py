import argparse
import sys
import logging

from pathlib import Path
from zoneinfo import reset_tzpath

from src.streamstats.analysis import analyze_events
from src.streamstats.errors import StreamStatsError, InvalidFormatError, InvalidCLIConfigurationError
from src.streamstats.parsers import execute
from src.streamstats.report import save_report

def main():
    parser = argparse.ArgumentParser(description="Поточный анализатор файлов")
    subparsers = parser.add_subparsers(dest="command",required=True)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("input", nargs = "+")
    analyze.add_argument("--format", required=True, choices=["csv","jsonl"])
    analyze.add_argument("--output", required=True)
    analyze.add_argument("--skip-invalid",action="store_true", help="Пропускать некорректные строки")

    args = parser.parse_args()
    try:
        if args.command == "analyze":
            result = analyze_events(args.input, skip_invalid=args.skip_invalid)
            save_report(result, args.output)
    except (StreamStatsError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())


