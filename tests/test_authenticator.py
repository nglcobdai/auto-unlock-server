from whisper import load_model

from server.utils import file_manager, settings


class Transcription:
    def __init__(self):
        self.model = load_model(settings.WHISPER_MODEL)

    def __call__(self, content):
        return self.model.transcribe(content)


class TestTranscription:
    @classmethod
    def setup_class(cls):
        cls.transcription = Transcription()

    def test_transcribe(self):
        with open("sample/test.wav", "rb") as file:
            content = file.read()
        file_manager.temporarily_save(content)
        result = self.transcription(str(file_manager.temp_file_path))
        file_manager.delete_temporary_file()

        assert result["text"] == "ひらけごま"
