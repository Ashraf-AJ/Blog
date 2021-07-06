import os
from api.cache.config import CacheDevelopmentConfig
from api.auth.config import Config as AuthConfig
from api.database.config import (
    Config as DatabaseConfig,
    DatabaseDevelopmentConfig,
    DatabaseTestingConfig,
)


class Config(AuthConfig, DatabaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ThisIsASecret"


class DevelopmentConfig(
    Config, CacheDevelopmentConfig, DatabaseDevelopmentConfig
):
    DEVELOPMENT = True


class TestingConfig(Config, DatabaseTestingConfig):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
