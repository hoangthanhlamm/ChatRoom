import pymongo
from settings import MONGODB_URL
import logging

connect = pymongo.MongoClient(MONGODB_URL)
db = connect["ChatRoom"]


class Account():
    async def create_user(self, body):
        acc = db["Account"]
        result = "Success"
        try:
            res = acc.insert_one(body)
            logging.info(res)
            return result
        except Exception as err:
            result = "Fail"
            logging.error(err)
            return result

    async def get_user(self, username):
        acc = db["Account"]
        try:
            res = acc.find_one({"username": username})
            logging.info(username)
            return res
        except Exception as err:
            logging.error(err)
            return None


class Message():
    async def save_msg(self, body):
        message = db["Message"]
        result = "Success"
        try:
            res = message.insert_one(body)
            logging.info(res)
            return result
        except Exception as err:
            result = "Fail"
            logging.error(err)
            return result

    async def load_msg(self, max_message):
        message = db["Message"]
        list_msg = []
        try:
            no_of_msg = message.count_documents({})
            res = message.find().sort("time", pymongo.ASCENDING).skip(no_of_msg - max_message).limit(max_message)
            for msg in res:
                list_msg.append(msg)
            return list_msg
        except Exception as err:
            logging.error(err)
            return None
