from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.utils.host_validation import HostValidationMiddleware


def create_client():
    app = FastAPI()
    app.add_middleware(HostValidationMiddleware)

    @app.get("/health")
    async def health():
        return {"ok": True}

    return TestClient(app)


def test_request_with_valid_host_header():
    client = create_client()

    response = client.get("/health", headers={"host": "example.com"})

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_request_without_host_header_is_rejected():
    client = create_client()

    response = client.get("/health", headers={"host": ""})

    assert response.status_code == 400
    assert response.text == "Invalid Host header"


def test_request_with_path_like_host_header_is_rejected():
    client = create_client()

    response = client.get("/health", headers={"host": "example.com/admin"})

    assert response.status_code == 400
    assert response.text == "Invalid Host header"
