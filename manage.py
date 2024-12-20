import uvicorn


if __name__ == '__main__':
    from src.configs.configuration import Configuration
    from src.configs.runtime_config import RuntimeConfig

    Configuration.apply(RuntimeConfig, alternative_env_search_dir=__file__)
    uvicorn.run(
        "manage_rest:app",
        access_log=RuntimeConfig.FASTAPI_ACCESS_LOG,
        backlog=RuntimeConfig.FASTAPI_BACKLOG,
        date_header=RuntimeConfig.FASTAPI_DATE_HEADER,
        forwarded_allow_ips=RuntimeConfig.FASTAPI_FORWARDED_ALLOW_IPS,
        host=RuntimeConfig.FASTAPI_SERVE_HOST,
        limit_concurrency=RuntimeConfig.FASTAPI_LIMIT_CONCURRENCY,
        limit_max_requests=RuntimeConfig.FASTAPI_LIMIT_MAX_REQUESTS,
        port=RuntimeConfig.FASTAPI_SERVE_PORT,
        proxy_headers=RuntimeConfig.FASTAPI_PROXY_HEADERS,
        reload=RuntimeConfig.FASTAPI_RELOAD,
        server_header=RuntimeConfig.FASTAPI_SERVER_HEADER,
        timeout_graceful_shutdown=RuntimeConfig.FASTAPI_TIMEOUT_GRACEFUL_SHUTDOWN,
        timeout_keep_alive=RuntimeConfig.FASTAPI_TIMEOUT_KEEP_ALIVE,
        workers=RuntimeConfig.FASTAPI_WORKERS_COUNT,
    )
