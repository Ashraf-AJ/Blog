from pathlib import Path

# Path(file).resolve().parent
# returns the top-level of the project
# where `file` is a file in the top level of the project.
BASE_DIR = Path("config.py").resolve().parent


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DatabaseDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        BASE_DIR.joinpath("dev_data.sqlite")
    )


class DatabaseTestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
