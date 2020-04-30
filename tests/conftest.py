import pytest

from src.web.api import create_app
from src.db.models import db


@pytest.fixture
def app():
    app = create_app({"TESTING": True,})
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
