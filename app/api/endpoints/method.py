from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.endpoints.switch_bot import SwitchBot
from app.config import settings
from app.api.endpoints.mongodb import MongoDB
import base64

ROOT_PATH = f"/api/{settings.API_VERSION}"

router = APIRouter()
switch_bot = SwitchBot()
mongo_db = MongoDB(
    host=settings.MONGODB_HOST_NAME,
    port=settings.MONGODB_PORT,
    root_user=settings.MONGODB_ROOT_USER_NAME,
    root_pwd=settings.MONGODB_ROOT_USER_PWD,
    db_name=settings.MONGODB_DATABASE,
    user_name=settings.MONGODB_USER_NAME,
    user_pwd=settings.MONGODB_USER_PWD,
)


class Record(BaseModel):
    voice: str


@router.post(f"{ROOT_PATH}/unlock")
async def unlock(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        base64_contents = base64.b64encode(contents).decode("utf-8")  # Base64エンコード
        mongo_db.create(
            "records",
            {
                "file_name": file.filename,
                "contents": base64_contents,
            },
        )

    except Exception as e:
        return JSONResponse(
            content={"message": "File upload failed", "error": str(e)}, status_code=400
        )

    return switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
