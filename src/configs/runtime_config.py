from src.configs.base_config import BaseConfig
from src.configs.base_fastapi_config import BaseFastAPIConfig


class RuntimeConfig(
    BaseConfig,
    BaseFastAPIConfig,
):
    FASTAPI_RE_DOCS_URL: str = None
    FASTAPI_DOCS_URL: str = None
    BASE_PRIVATE_RATE_LIMIT_REQUEST_COUNT: int = 1000
    BASE_PRIVATE_RATE_LIMIT_REQUEST_INTERVAL_SECONDS: int = 1
    BASE_PUBLIC_RATE_LIMIT_REQUEST_COUNT: int = 1000
    BASE_PUBLIC_RATE_LIMIT_REQUEST_INTERVAL_SECONDS: int = 1
