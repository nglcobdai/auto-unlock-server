import base64

from fastapi.responses import JSONResponse

from app.api.src.authenticator import SecretPhraseAuthenticator
from app.api.src.mongodb import MongoDB
from app.api.src.switch_bot import SwitchBot
from app.utils.config import settings

authenticator = SecretPhraseAuthenticator()
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


async def unlock_manager(file):
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

    is_auth = authenticator(contents)
    if is_auth:
        return switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
    return {"message": f"Authentication failed, result: {authenticator.result['text']}"}
