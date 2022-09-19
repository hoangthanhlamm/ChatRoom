import pymongo
from settings import MONGODB_URL
import logging

connect = pymongo.MongoClient(MONGODB_URL)
db = connect["ChatRoom"]


class Account:
    def __init__(self):
        self.collection = db["Account"]

    async def create_user(self, body):
        result = "Success"
        try:
            res = self.collection.insert_one(body)
            logging.info(res)
        except Exception as err:
            result = "Fail"
            logging.error(err)
        return result

    async def get_user(self, username):
        try:
            res = self.collection.find_one({"username": username})
            logging.info(username)
            return res
        except Exception as err:
            logging.error(err)
        return None


class Message:
    def __init__(self):
        self.collection = db["Message"]

    async def save_msg(self, body):
        result = "Success"
        try:
            res = self.collection.insert_one(body)
            logging.info(res)
        except Exception as err:
            result = "Fail"
            logging.error(err)
        return result

    async def load_msg(self, max_message):
        list_msg = []
        try:
            no_of_msg = self.collection.count_documents({})
            skip = no_of_msg - max_message if max_message < no_of_msg else 0
            res = self.collection.find().sort("time", pymongo.ASCENDING).skip(skip).limit(max_message)
            for msg in res:
                list_msg.append(msg)
            return list_msg
        except Exception as err:
            logging.error(err)
        return None
