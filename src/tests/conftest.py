import pytest
from app import create_app, config, db


@pytest.fixture(scope="session", autouse=True)
def app():
    """Create app for testing"""
    app = create_app(config.TestConfig)
    yield app
    with app.app_context():
        db.session.remove()


@pytest.fixture(scope="module")
def client(app):
    """Create test client to pass as an argument to other tests"""

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.drop_all()
        db.create_all()
