from pymongo import MongoClient

from bot import LOGGER, AUTHORIZED_USERS, DATABASE_URL

class DatabaseHelper:

    def __init__(self):
        self.__err = False
        self.__client = None
        self.__db = None
        self.__collection = None
        self.__connect()

    def __connect(self):
        try:
            self.__client = MongoClient(DATABASE_URL)
            self.__db = self.client['SearchX']
            self.__collection = self.db['users']
        except PyMongoError as err:
            LOGGER.error(err)
            self.__err = True

    def auth_user(self, user_id: int):
        if self.__err:
            return
        self.col.insert_one({"user_id": user_id})
        return 'Authorization granted'
        self.__client.close()

    def unauth_user(self, user_id: int):
        if self.__err:
            return
        self.col.delete_many({"user_id": user_id})
        return 'Authorization revoked'
        self.__client.close()

    def load_users(self):
        if self.__err:
            return
        users = self.col.find().sort("user_id")
        for user in users:
            AUTHORIZED_USERS.add(user["user_id"])
        self.__client.close()

if DATABASE_URL is not None:
    DatabaseHelper().load_users()
