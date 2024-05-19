from fastapi import APIRouter, File, UploadFile

from app.api.endpoints.unlock import unlock_manager
from app.api.src.switch_bot import SwitchBot
from app.utils.config import settings

ROOT_PATH = f"/api/{settings.API_VERSION}"

router = APIRouter()
switch_bot = SwitchBot()


@router.post(f"{ROOT_PATH}/unlock")
async def unlock(file: UploadFile = File(None)):
    if file is None:
        return switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
    return await unlock_manager(file)
