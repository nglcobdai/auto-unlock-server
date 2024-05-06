import requests
import json
import dotenv
import os
import time
import hashlib
import hmac
import base64
from logging import getLogger


logger = getLogger(__name__)


class SwitchBot:
    SWITCH_BOT_API_URL = "https://api.switch-bot.com"
    VERSION = "v1.1"

    def __init__(self):
        dotenv.load_dotenv(".env")  # .envファイルをロードする

        switch_bot_token = os.getenv("SWITCH_BOT_TOKEN")
        switch_bot_secret = os.getenv("SWITCH_BOT_SECRET")
        self.unlock_bot_id = os.getenv("UNLOCK_BOT_ID")

        nonce = ""
        t = int(round(time.time() * 1000))
        string_to_sign = "{}{}{}".format(switch_bot_token, t, nonce)

        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(switch_bot_secret, "utf-8")

        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest(),
        )

        self.headers = {
            "Authorization": switch_bot_token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce,
            "Content-Type": "application/json; charset=utf8",
        }

        self.device_list = self.get_device_list()

    def _get_request(self, url):
        res = requests.get(url, headers=self.headers)
        data = res.json()
        if data["message"] == "success":
            logger.info(f"Successfully GET request to {url}")
            return res.json()
        logger.error(f"Failed GET request to {url}")
        return {}

    def _post_request(self, url, params):
        res = requests.post(url, data=json.dumps(params), headers=self.headers)
        data = res.json()
        message = data.get("message", None)
        if message == "success":
            logger.info(f"Successfully POST request to {url}, params: {params}")
        else:
            logger.error(
                f"Failed POST request to {url}, params: {params}, res: {message}"
            )
        return data

    def get_device_list(self):
        url = f"{self.SWITCH_BOT_API_URL}/{self.VERSION}/devices"
        try:
            res = self._get_request(url)["body"]
            return res
        except Exception:
            return {}

    def control_device(self, deviceId, command):
        url = f"{self.SWITCH_BOT_API_URL}/{self.VERSION}/devices/{deviceId}/commands"
        params = {
            "command": command,
            "parameter": "",
            "commandType": "command",
        }
        return self._post_request(url, params)


if __name__ == "__main__":
    switch_bot = SwitchBot()
    switch_bot.control_device(switch_bot.unlock_bot_id, "turnOn")
