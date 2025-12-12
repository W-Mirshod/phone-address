import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_redis


class FakeRedis:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value):
        self.store[key] = value
        return True

    async def exists(self, key):
        return 1 if key in self.store else 0

    async def delete(self, key):
        return 1 if self.store.pop(key, None) is not None else 0


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def client(fake_redis):
    app.dependency_overrides[get_redis] = lambda: fake_redis
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_get_address_not_found(client):
    response = client.get("/phones/+1234567890")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_phone_address_success(client):
    data = {"phone": "+1234567890", "address": "123 Main St"}
    response = client.post("/phones", json=data)
    assert response.status_code == 201
    assert response.json()["phone"] == "+1234567890"
    assert response.json()["address"] == "123 Main St"


def test_create_phone_address_conflict(client):
    data = {"phone": "+1234567890", "address": "123 Main St"}
    client.post("/phones", json=data)
    response = client.post("/phones", json=data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_get_address_success(client):
    data = {"phone": "+1234567890", "address": "123 Main St"}
    client.post("/phones", json=data)
    response = client.get("/phones/+1234567890")
    assert response.status_code == 200
    assert response.json()["phone"] == "+1234567890"
    assert response.json()["address"] == "123 Main St"


def test_update_address_success(client):
    data = {"phone": "+1234567890", "address": "123 Main St"}
    client.post("/phones", json=data)
    update_data = {"address": "456 Oak Ave"}
    response = client.put("/phones/+1234567890", json=update_data)
    assert response.status_code == 200
    assert response.json()["phone"] == "+1234567890"
    assert response.json()["address"] == "456 Oak Ave"


def test_update_address_not_found(client):
    update_data = {"address": "456 Oak Ave"}
    response = client.put("/phones/+1234567890", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_phone_address_success(client):
    data = {"phone": "+1234567890", "address": "123 Main St"}
    client.post("/phones", json=data)
    response = client.delete("/phones/+1234567890")
    assert response.status_code == 204
    get_response = client.get("/phones/+1234567890")
    assert get_response.status_code == 404


def test_delete_phone_address_not_found(client):
    response = client.delete("/phones/+1234567890")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

