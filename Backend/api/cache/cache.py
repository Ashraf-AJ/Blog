import redis


class Cache:
    def __init__(self):
        self.jwt_blocklist = None

    def init_app(self, app):
        self.jwt_blocklist = redis.Redis(
            host=app.config.get("CACHE_HOST"),
            port=app.config.get("CACHE_PORT"),
            db=app.config.get("CACHE_DB_NUMEBR"),
            decode_responses=True,
        )
