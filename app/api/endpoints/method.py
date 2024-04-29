from fastapi import APIRouter
from app.api.endpoints.switch_bot import SwitchBot

router = APIRouter()
switch_bot = SwitchBot()


@router.post("/api/unlock")
def unlock():
    return switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
