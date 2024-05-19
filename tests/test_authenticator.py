# tests/test_import_whisper.py
# import whisper

# from app.api.src.transcription import Transcription


from whisper import load_model

from app.utils.config import settings


class Transcription:
    def __init__(self):
        self.model = load_model(settings.WHISPER_MODEL)

    def __call__(self, content):
        return self.model.transcribe(content)


def test_import_whisper():
    tran = Transcription()
    # model = whisper.load_model("small")
    test_file_path = "sample/test.wav"

    assert tran(test_file_path)["text"] == "ひらけごま"
