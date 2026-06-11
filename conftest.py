import pytest
from utils.savanna_client import SavannaClient
from utils.wait_utils import ensure_workspace_active


@pytest.fixture(scope="session")
def client():
    client = SavannaClient()
    return client


@pytest.fixture(scope="session", autouse=True)
def workspace_active(client):
    ensure_workspace_active(client)