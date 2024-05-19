from app.utils.file_manager import FileManager

from whisper import load_model

from app.utils.config import settings


class Transcription:
    def __init__(self):
        self.model = load_model(settings.WHISPER_MODEL)

    def __call__(self, content):
        return self.model.transcribe(content)


class TestTranscription:
    @classmethod
    def setup_class(cls):
        cls.transcription = Transcription()
        cls.file_manager = FileManager()

    def test_transcribe(self):
        with open("sample/test.wav", "rb") as file:
            content = file.read()
        self.file_manager.temporarily_save(content)
        result = self.transcription(str(self.file_manager.temp_file_path))
        self.file_manager.delete_temporary_file()

        assert result["text"] == "ひらけごま"
