# Лабораторная работа №2. Потоковый анализатор файлов.

**Матюшин Всеволод Алексеевич, группа М8О-102БВ-26**

## Структура проекта

 <pre>
src/streamstats  
├── __init__.py
├── __main__.py             # CLI
├── analysis.py             # Анализатор
├── errors.py               # Ошибки
├── models.py               # Модель события и проверка данных.
├── parsers.py              # Парсеры csv и jsonl файлов
├── report.py               # Json-отчёт
tests/
├── test_analysis.py        # Тесты анализатора
├── test_cli.py             # Тесты CLI
├── test_models.py          # Тесты моделей событий
├── test_parsers.py         # Тесты csv и jsonl парсеров
├── test_report.py          # Тесты отчётов
</pre>

## Схема работы парсера:
**1) Проверка формата файлов (`check_format`) - проверяет формат исходных файлов, если это не csv или не jsonl, то выводит ошибку**

**2) csv-парсер (`csv_parser`) - парсит csv файл**

**3) jsonl-парсер (`jsonl_parser`) - парсит jsonl файл**


## Схема работы анализатора:
**1) Анализатор событий (`analyze_events`) - потоковый анализ событий: подсчитывает статистику, 
находит временные границы и определяет топ-5 источников ошибок.**


## Схема работы составления отчета:
**1) Отчёт (`save_report`) - сохраняет результаты анализа в JSON-файл с поддержкой Unicode.**


# Поддерживается:
`CSV` — чтение и обработка файлов формата `.csv`.
`JSONL` — чтение и обработка файлов формата `.jsonl`.

`Event` — проверка корректности событий:
- `timestamp` — дата и время в формате ISO 8601
- `level` — уровни `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `source` — источник события
- `message` — текст сообщения

`Analyzer` — потоковый анализ событий:
- Подсчёт общего количества событий.
- Статистика по уровням и источникам.
- Топ-5 источников ошибок (`ERROR`, `CRITICAL`).
- Определение первой и последней временной отметки.
- Пропуск некорректных строк при использовании `--skip-invalid`.

`Report` — сохранение результатов анализа в JSON с поддержкой Unicode.
`CLI` — запуск анализа через командную строку с указанием входных файлов, формата и пути сохранения отчёта.

# Использование через терминал:

`python -m streamstats --help`
    
`python -m pytest`

`python -m pytest --cov=src.streamstats --cov-report=term-missing`

`ruff check .`

`python -m streamstats analyze events.csv --format csv --output report.json`

`python -m streamstats analyze events.jsonl --format jsonl --output report.json`

`python -m streamstats analyze events.csv --format csv --output report.json --skip-invalid`

`python -m streamstats analyze missing.csv --format csv --output report.json`


# Тесты через терминал:
**Анализатор CSV:**
<pre>
python -m streamstats analyze events.csv --format csv --output report.json -> Создание отчёта report.json
python -m streamstats analyze events.csv --format csv --output report.json --skip-invalid -> Пропуск некорректных строк
</pre>

**Анализатор JSONL:**
<pre>
python -m streamstats analyze events.jsonl --format jsonl --output report.json -> Создание отчёта report.json
python -m streamstats analyze events.jsonl --format jsonl --output report.json --skip-invalid -> Пропуск некорректных строк
</pre>

**Проверка ошибок:**
<pre>
python -m streamstats analyze missing.csv --format csv --output report.json -> Ошибка: файл не найден
python -m streamstats analyze events.txt --format csv --output report.json -> Ошибка: неподдерживаемый формат файла
</pre>


# Функционал:
- Чтение и обработка файлов форматов `CSV` и `JSONL`.
- Проверка корректности событий: даты и времени (`timestamp`), уровня события (`level`), источника (`source`) и сообщения (`message`).
- Поточный анализ данных без загрузки всего файла в память.
- Подсчёт общего количества обработанных событий.
- Подсчёт количества событий по уровням: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- Подсчёт количества событий по источникам (`source`).
- Определение топ-5 источников событий с уровнями `ERROR` и `CRITICAL`.
- Определение самой ранней и самой поздней временной отметки.
- Обработка нескольких входных файлов с объединением результатов анализа.
- Возможность пропускать некорректные строки с помощью параметра `--skip-invalid`.
- Сохранение результатов анализа в JSON-файл с поддержкой Unicode.
- Работа через терминал: запуск анализа, указание формата и входных файлов, выбор пути сохранения отчёта, вывод ошибок и предупреждений.
