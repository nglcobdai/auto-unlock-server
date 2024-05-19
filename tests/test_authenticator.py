# from unittest import TestCase

# from app.api.src.authenticator import SecretPhraseAuthenticator


# class TestSecretPhraseAuthenticator(TestCase):
#     def setup_class(cls):
#         cls.authenticator = SecretPhraseAuthenticator()
#         cls.test_file_path = "sample/test.wav"

#     def test_call(self):
#         with open(self.test_file_path, "rb") as f:
#             content = f.read()
#         assert self.authenticator(content, "ひらけごま")
