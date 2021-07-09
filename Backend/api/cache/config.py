import os


class CacheDevelopmentConfig:
    CACHE_HOST = os.environ.get("CACHE_HOST") or "localhost"
    CACHE_PORT = os.environ.get("CACHE_PORT") or 6379
    CACHE_DB = os.environ.get("CACHE_DB_NUMEBR") or 0
