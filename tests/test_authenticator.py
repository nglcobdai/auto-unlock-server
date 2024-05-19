from app.api.src.authenticator import SecretPhraseAuthenticator


class TestSecretPhraseAuthenticator:
    @classmethod
    def setup_class(cls):
        cls.secret_phrase_authenticator = SecretPhraseAuthenticator()

        with open("sample/test.wav", "rb") as file:
            cls.content = file.read()

    def test_is_authenticated(self):
        assert self.secret_phrase_authenticator(self.content) is True
