import pytest

from src.web.api import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True,})

    with app.app_context():
        pass

    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
