from fastapi import Depends, FastAPI, HTTPException, WebSocketException, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

from src.configs.runtime_config import RuntimeConfig

bearer_scheme = HTTPBearer()

base_responses = {
    400: {"description": "Invalid Input Arguments"},
    504: {"description": "Request Process Timed Out"},
    404: {"description": "Requested Resource Not Found"},
    409: {"description": "Requested Entity Already Exists or Faced a conflict"},
    429: {"description": "Too Many Requests Sent"},
    503: {"description": "Service Temporary Unavailable"},
    501: {"description": "Requested Method Not Implemented"},
    500: {"description": "Internal Server Error"},
}


def _create_app():
    from src.configs.configuration import Configuration

    from src.configs.runtime_config import RuntimeConfig

    Configuration.apply(RuntimeConfig, alternative_env_search_dir=__file__)
    app = FastAPI(
        openapi_url=RuntimeConfig.FASTAPI_OPENAPI_URL,
        docs_url=RuntimeConfig.FASTAPI_DOCS_URL,
        redocs_url=RuntimeConfig.FASTAPI_RE_DOCS_URL,
    )
    _add_routers(app)
    _add_middleware(app)
    return app


def _add_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=RuntimeConfig.FASTAPI_CORS_MIDDLEWARE_ALLOW_ORIGINS,
        allow_credentials=RuntimeConfig.FASTAPI_CORS_MIDDLEWARE_ALLOW_CREDENTIALS,
        allow_methods=RuntimeConfig.FASTAPI_CORS_MIDDLEWARE_ALLOW_METHODS,
        allow_headers=RuntimeConfig.FASTAPI_CORS_MIDDLEWARE_ALLOW_HEADERS,
    )


def _add_routers(app):
    _add_public_router(app)
    _add_basic_router(app)


def _add_public_router(app):
    from src.services.v1.public_services_v1 import public_router_v1

    responses = base_responses
    app.include_router(public_router_v1, prefix="/api/v1", responses=responses)


def _add_basic_router(app):
    from src.services.base_services import base_router

    app.include_router(base_router, prefix="")


app = _create_app()
