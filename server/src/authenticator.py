from pathlib import Path

from Levenshtein import ratio

from server.src.transcription import Transcription
from server.utils import file_manager, settings


class SecretPhraseAuthenticator:
    def __init__(self):
        self.secret_phrase = settings.SECRET_PHRASE
        self.transcription = Transcription()
        self.file_manager = file_manager

        temporary_file_dir = Path(settings.DATADRIVE) / "temp"
        temporary_file_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file_path = temporary_file_dir / "temp.wav"

    def __is_authenticated(self, phrase, secret_phrase=None):
        secret_phrase = secret_phrase or self.secret_phrase
        self.score = ratio(phrase, secret_phrase)
        return self.score > settings.AUTHENTICATION_THRESHOLD

    def __call__(self, content, secret_phrase=None):
        self.file_manager.temporarily_save(content)
        self.result = self.transcription(str(self.file_manager.temp_file_path))
        self.context = self.result["text"]
        self.file_manager.delete_temporary_file()
        return self.__is_authenticated(self.result["text"], secret_phrase)
