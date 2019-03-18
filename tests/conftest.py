import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa: E402

from app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def test_client(app, app_context):
    return app.test_client()
