from pathlib import Path

from Levenshtein import ratio

from app.api.src.transcription import Transcription
from app.utils.config import settings
from app.utils.file_manager import FileManager


class SecretPhraseAuthenticator:
    def __init__(self):
        self.secret_phrase = settings.SECRET_PHRASE
        self.transcription = Transcription()
        self.file_manager = FileManager()

        temporary_file_dir = Path(settings.DATADRIVE) / "temp"
        temporary_file_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file_path = temporary_file_dir / "temp.wav"

    def __is_authenticated(self, phrase, secret_phrase=None):
        secret_phrase = secret_phrase or self.secret_phrase
        self.ratio = ratio(phrase, secret_phrase)
        return self.ratio > settings.AUTHENTICATION_THRESHOLD

    def __call__(self, content, secret_phrase=None):
        self.file_manager.temporarily_save(content)
        self.result = self.transcription(str(self.file_manager.temp_file_path))
        self.context = self.result["text"]
        self.file_manager.delete_temporary_file()
        return self.__is_authenticated(self.result["text"], secret_phrase)
