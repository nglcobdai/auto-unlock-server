import base64
from time import time

from fastapi import BackgroundTasks

from server.src.authenticator import SecretPhraseAuthenticator
from server.src.mongodb import MongoDB
from server.src.switch_bot import SwitchBot
from server.utils import logger, settings


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
        self.call_bot_time = None

    async def __call__(
        self, file=None, background_tasks: BackgroundTasks = BackgroundTasks()
    ):
        self.check_timeout()
        if (file) and (self.is_phase_unlock):
            logger.info("Unlocking the bot process is called")
            return await self.control_unlock_bot(file, background_tasks)
        elif (file is None) and (self.is_phase_unlock):
            return {
                "message": "File is required",
                "phrase_authorized": self.is_phase_unlock,
            }
        elif (file) and (not self.is_phase_unlock):
            return {
                "message": "File is not required",
                "phrase_authorized": self.is_phase_unlock,
            }

        logger.info("Calling the bot process is called")
        return self.control_call_bot()

    def check_timeout(self):
        if self.call_bot_time is None:
            return
        now = time()
        if (now - self.call_bot_time) > settings.TIMEOUT:
            self.is_phase_unlock = False
            self.call_bot_time = None

    def control_call_bot(self):
        response = self.switch_bot.control_device(settings.CALL_BOT_ID, "turnOn")
        self.is_phase_unlock = response["message"] == "success"
        response["phrase_authorized"] = self.is_phase_unlock
        self.call_bot_time = time()
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
            logger.info(
                f"Authentication succeeded, result: {self.authenticator.context}, score: {self.authenticator.score}"
            )
            response = self.switch_bot.control_device(settings.UNLOCK_BOT_ID, "turnOn")
            response["phrase_authorized"] = True
            response["result"] = self.authenticator.context
            response["score"] = self.authenticator.score

            return response

        message = f"Authentication failed, result: {self.authenticator.context},\
            not {settings.SECRET_PHRASE}, score: {self.authenticator.score}"
        logger.error(message)
        return {"message": message}

    async def save_to_db(self, filename, base64_contents):
        try:
            self.mongo_db.create(
                "records",
                {
                    "file_name": filename,
                    "context": self.authenticator.context,
                    "contents": base64_contents,
                },
            )
        except Exception as e:
            logger.error(f"Failed to save data to MongoDB: {e}")
