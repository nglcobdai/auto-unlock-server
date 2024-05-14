from pymongo import MongoClient
from dotenv import load_dotenv
import os
from logging import getLogger
from time import time


load_dotenv()
logger = getLogger(__name__)

HOST_NAME = os.getenv("MONGODB_HOST_NAME")
PORT_NUM = int(os.getenv("MONGODB_PORT"))
ROOT_USER_NAME = os.getenv("MONGODB_ROOT_USER_NAME")
ROOT_USER_PWD = os.getenv("MONGODB_ROOT_USER_PWD")
DB_NAME = os.getenv("MONGODB_DATABASE")
USER_NAME = os.getenv("MONGODB_USER_NAME")
USER_PWD = os.getenv("MONGODB_USER_PWD")


class MongoDB:
    def __init__(self, host, port, root_user, root_pwd, db_name, user_name, user_pwd):
        """MongoDB class

        Args:
            host (str): Host name
            port (int): Port number
            root_user (str): Root user name
            root_pwd (str): Root user password
            db_name (str): Database name
            user_name (str): User name
            user_pwd (str): User password
        """
        self.client = MongoClient(
            host=host, port=port, username=root_user, password=root_pwd
        )
        self.db = self.client[db_name]

        # ユーザーが存在しない場合は作成
        user_list = self.db.command("usersInfo").get("users", [])
        if not any(user["user"] == user_name for user in user_list):
            self.__create_user(user_name, user_pwd)

        # コレクションが存在しない場合は作成
        collection_list = self.db.list_collection_names()
        if db_name not in collection_list:
            self.__create_collection(db_name)
        else:
            logger.warning(f"Collection '{db_name}' already exists")

    def __create_user(self, user_name, user_pwd, role="readWrite"):
        """Create user

        Args:
            user_name (str): User name
            user_pwd (str): User password
            role (str, optional): Role ("readWrite").
        """
        self.db.command(
            "createUser",
            user_name,
            pwd=user_pwd,
            roles=[{"role": role, "db": self.db.name}],
        )

    def __create_collection(self, collection_name):
        """Create collection

        Args:
            collection_name (str): Collection name
        """
        self.db.create_collection(collection_name)

    def create(self, collection_name, data):
        """Create data

        Args:
            collection_name (str): Collection name
            data (dict): data
        """
        record = {"timestamp": time(), **data}
        self.db[collection_name].insert_one(record)

    def read_all(self, collection_name):
        """Read all records

        Args:
            collection_name (str): Collection name

        Returns:
            list: Record list
        """
        return list(self.db[collection_name].find())

    def count_all(self, collection_name):
        """Count all records

        Args:
            collection_name (str): Collection name

        Returns:
            int: Number of records
        """
        return self.db[collection_name].count_documents({})

    def __del__(self):
        """デストラクタ"""
        self.client.close()


if __name__ == "__main__":
    try:
        MongoDB(
            host=HOST_NAME,
            port=PORT_NUM,
            root_user=ROOT_USER_NAME,
            root_pwd=ROOT_USER_PWD,
            db_name=DB_NAME,
            user_name=USER_NAME,
            user_pwd=USER_PWD,
        )
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
