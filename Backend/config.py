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
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.gmail.com"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER") or "sender@example.com"
    )


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
