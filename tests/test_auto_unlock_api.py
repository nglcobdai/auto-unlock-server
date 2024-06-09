from time import sleep

from fastapi.testclient import TestClient

from server.main import server
from server.utils.config import settings


class TestAutoUnlockAPI:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(server)
        cls.endpoint_url = f"/{settings.API_VERSION}/unlock"

    def test_post_without_file(self):
        response = self.client.post(self.endpoint_url)

        assert response.status_code == 200

    def test_post_with_file(self):
        _ = self.client.post(self.endpoint_url)
        files = {"file": ("test.wav", open("sample/test.wav", "rb"), "audio/wav")}
        response = self.client.post(self.endpoint_url, files=files)

        assert response.status_code == 200

    def test_post_timeout(self):
        _ = self.client.post(self.endpoint_url)

        sleep(settings.TIMEOUT)

        files = {"file": ("test.wav", open("sample/test.wav", "rb"), "audio/wav")}
        response = self.client.post(self.endpoint_url, files=files)

        assert response.json()["phrase_authorized"] is False
