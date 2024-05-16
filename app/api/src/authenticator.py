from pathlib import Path


from app.config import settings
from app.api.src.transcription import Transcription


class SecretPhraseAuthenticator:
    def __init__(self):
        self.secret_phrase = settings.SECRET_PHRASE
        self.transcription = Transcription()

        temporary_file_dir = Path(settings.DATADRIVE) / "temp"
        temporary_file_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file_path = temporary_file_dir / "temp.wav"

    def __temporarily_save(self, content):
        with open(self.temp_file_path, "wb") as temp_file:
            temp_file.write(content)

    def __delete_temporary_file(self):
        self.temp_file_path.unlink()

    def __is_authenticated(self, secret_phrase):
        return secret_phrase == self.secret_phrase

    def __call__(self, content):
        self.__temporarily_save(content)
        result = self.transcription(str(self.temp_file_path))
        self.__delete_temporary_file()
        return self.__is_authenticated(result)
