from fastapi import APIRouter
from app.api.endpoints.switch_bot import SwitchBot
from app.config import settings

ROOT_PATH = f"/api/{settings.API_VERSION}"

router = APIRouter()
switch_bot = SwitchBot()


@router.post(f"{ROOT_PATH}/unlock")
def unlock():
    return switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
