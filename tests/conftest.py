
import pytest
from fastapi.testclient import TestClient

from github_users.api.service import UserService
from github_users.settings import Settings


@pytest.fixture
def settings():
    return Settings(name="IntegrationTest")


@pytest.fixture
def test_service(settings):
    return UserService(settings=settings)


@pytest.fixture
def test_client(test_service):
    yield TestClient(test_service)
