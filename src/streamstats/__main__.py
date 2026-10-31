import argparse
import sys

from src.streamstats.analysis import analyze_events
from src.streamstats.errors import StreamStatsError
from src.streamstats.report import save_report


def main():

    """Функция `main()` отвечает за запуск программы через командную строку.

    Настраивает аргументы для выбора входных файлов, формата данных (`CSV` или `JSONL`),
    пути сохранения отчёта и режима пропуска некорректных строк.

    Запускает анализ файлов, передаёт результаты для сохранения в JSON.

    При возникновении ошибок выводит сообщение в консоль и возвращает код завершения `2`,
    при успешном выполнении — `0`."""

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


