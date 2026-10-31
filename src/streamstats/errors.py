class StreamStatsError(Exception):
    """"Базовая ошибка StreamStatsError"""


class InvalidFormatError(StreamStatsError):
    """"Ошибка формата"""


class InvalidEventError(StreamStatsError):
    """"Ошибка события"""


class InvalidTimeMarkError(InvalidEventError):
    """Ошибка метки времени"""


class InvalidCLIConfigurationError(StreamStatsError):
    """"Ошибка конфигурации CLI"""

