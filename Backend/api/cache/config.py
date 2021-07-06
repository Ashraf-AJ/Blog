import os


class CacheDevelopmentConfig:
    Cache_HOST = os.environ.get("Cache_HOST") or "localhost"
    Cache_PORT = os.environ.get("Cache_PORT") or 6379
    Cache_DB = os.environ.get("Cache_DB_NUMEBR") or 0
