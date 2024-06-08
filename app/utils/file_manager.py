from pathlib import Path

from app.utils.config import settings


class FileManager:
    def __init__(self):
        temporary_file_dir = Path(settings.DATADRIVE) / "temp"
        temporary_file_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file_path = temporary_file_dir / "temp.wav"

    def temporarily_save(self, content):
        with open(self.temp_file_path, "wb") as temp_file:
            temp_file.write(content)

    def delete_temporary_file(self):
        self.temp_file_path.unlink()
