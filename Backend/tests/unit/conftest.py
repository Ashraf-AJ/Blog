import pytest
from app import create_app
from api import db as database


@pytest.fixture(scope="package")
def test_app():
    return create_app("testing")


@pytest.fixture(scope="module")
def db(test_app):
    with test_app.app_context():
        database.drop_all()
        database.create_all()
        yield database
        database.drop_all()
