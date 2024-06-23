from server.utils.config import Settings
from server.utils.file_manager import FileManager
from server.utils.log import Logger

settings = Settings()
logger = Logger("Auto Unlock Server").logger
file_manager = FileManager(settings.DATADRIVE)
