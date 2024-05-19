from fastapi.testclient import TestClient

from app.utils.config import settings
from app.main import app


class TestAutoUnlockAPI:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
        cls.endpoint_url = f"/api/{settings.API_VERSION}/unlock"

    def test_post_without_file(self):
        response = self.client.post(self.endpoint_url)

        assert response.status_code == 200

    def test_post_with_file(self):
        files = {"file": ("test.wav", open("sample/test.wav", "rb"), "audio/wav")}
        response = self.client.post(self.endpoint_url, files=files)

        assert response.status_code == 200
