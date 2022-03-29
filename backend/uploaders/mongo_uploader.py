from pymongo import MongoClient
from time import localtime, strftime
import urllib.parse


class mongo_uploader():
    def __init__(self, ip, port, user, passwd, db, collection):
        username = urllib.parse.quote_plus(user)
        password = urllib.parse.quote_plus(passwd)
        self.client = MongoClient('mongodb://%s:%s@%s:%s' % (username, password, ip, port))
        self.db = self.client[db]
        self.colection = self.db[collection]

    def upload_json(self, filename, tags):
        time_now = strftime("%Y-%m-%d %H:%M:%S", localtime())
        meta_mongo = {
            'file': filename,
            'tags': tags,
            'time': time_now
        }
        return self.colection.insert_one(meta_mongo).inserted_id
    def get_all_files(self):
        cursor = self.colection.find({})
        result = []
        for item in cursor:
            result.append(item)
        return result
