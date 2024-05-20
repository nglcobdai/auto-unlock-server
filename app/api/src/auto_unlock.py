import base64
from logging import getLogger

from fastapi import BackgroundTasks

from app.api.src.authenticator import SecretPhraseAuthenticator
from app.api.src.mongodb import MongoDB
from app.api.src.switch_bot import SwitchBot
from app.utils.config import settings

logger = getLogger(__name__)


class AutoUnlock:
    def __init__(self):
        self.is_phase_unlock = False
        self.switch_bot = SwitchBot()
        self.authenticator = SecretPhraseAuthenticator()
        self.mongo_db = MongoDB(
            host=settings.MONGODB_HOST_NAME,
            port=settings.MONGODB_PORT,
            root_user=settings.MONGODB_ROOT_USER_NAME,
            root_pwd=settings.MONGODB_ROOT_USER_PWD,
            db_name=settings.MONGODB_DATABASE,
            user_name=settings.MONGODB_USER_NAME,
            user_pwd=settings.MONGODB_USER_PWD,
        )

    async def __call__(
        self, file=None, background_tasks: BackgroundTasks = BackgroundTasks()
    ):
        if (file) and (self.is_phase_unlock):
            return await self.control_unlock_bot(file, background_tasks)
        if (file is None) and (not self.is_phase_unlock):
            return self.control_call_bot()
        return {"message": "Invalid request"}

    def control_call_bot(self):
        response = self.switch_bot.control_device(settings.CALL_BOT_ID, "turnOn")
        self.is_phase_unlock = response["message"] == "success"
        response["phrase_authorized"] = self.is_phase_unlock
        return response

    async def control_unlock_bot(self, file, background_tasks):
        response = await self.unlock_manager(file, background_tasks)
        self.is_phase_unlock = not (response["message"] == "success")
        response["phrase_authorized"] = self.is_phase_unlock
        return response

    async def unlock_manager(self, file, background_tasks):
        contents = await file.read()
        base64_contents = base64.b64encode(contents).decode("utf-8")  # Base64エンコード
        is_auth = self.authenticator(contents)

        # データベース操作をバックグラウンドタスクに登録
        background_tasks.add_task(self.save_to_db, file.filename, base64_contents)

        if is_auth:
            return self.switch_bot.control_device(settings.UNLOCK_BOT_ID, "turnOn")
        logger.error(f"Authentication failed, result: {self.authenticator.context}")
        return {
            "message": f"Authentication failed, result: {self.authenticator.context}"
        }

    async def save_to_db(self, filename, base64_contents):
        try:
            self.mongo_db.create(
                "records",
                {
                    "file_name": filename,
                    "context": self.authenticator.result["text"],
                    "contents": base64_contents,
                },
            )
        except Exception as e:
            # ロギングや他のエラーハンドリングが必要であればここに追加
            logger.error(f"Failed to save data to MongoDB: {e}")
