import logging


class BaseConfig:
    LOGGING_LEVEL: int = logging.WARNING
    SERVE_HOST: str = 'localhost'
    SERVE_PORT: int = '8100'
    DEBUG: bool = True
