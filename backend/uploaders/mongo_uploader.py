from pymongo import MongoClient
from time import localtime, strftime

class mongo_uploader():
    def __init__(self, ip, port, db, collection):
        self.client = MongoClient(ip, int(port))
        self.db = self.client[db]
        self.colection = self.db[collection]
    def upload_json(self, filename,tags):
        time_now = strftime("%Y-%m-%d %H:%M:%S", localtime())
        meta_mongo = {
            'file': filename,
            'tags': tags,
            'time': time_now
        }
        return self.colection.insert_one(meta_mongo).inserted_id
