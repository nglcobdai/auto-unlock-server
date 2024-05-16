from whisper import load_model

from app.config import settings


class Transcription:
    def __init__(self):
        self.model = load_model(settings.WHISPER_MODEL)

    def __call__(self, content):
        return self.model.transcribe(content)
