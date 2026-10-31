class StreamStatsError(Exception):
    """"Базовая ошибка StreamStatsError"""
    pass


class InvalidFormatError(StreamStatsError):
    """"Ошибка формата"""
    pass


class InvalidEventError(StreamStatsError):
    """"Ошибка события"""
    pass


class InvalidTimeMarkError(StreamStatsError):
    """"Ошибка метки времени"""
    pass


class InvalidCLIConfigurationError(StreamStatsError):
    """"Ошибка конфигурации CLI"""
    pass

