from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


class TestAutoUnlockAPI:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_post(self):
        endpoint_url = f"/api/{settings.API_VERSION}/unlock"
        files = {"file": ("test.wav", open("sample/test.wav", "rb"), "audio/wav")}
        response = self.client.post(endpoint_url, files=files)

        assert response.status_code == 200
