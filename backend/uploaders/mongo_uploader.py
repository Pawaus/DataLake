import socket

from pymongo import MongoClient
from time import localtime, strftime
import urllib.parse
import os


class mongo_uploader():
    def __init__(self):
        self.isProd = bool(os.getenv('DEVELOPMENT_FLASK', True))
        if self.isProd:
            try:
                self.ip_mongo = socket.gethostbyname('mongo_db')
            except:
                self.ip_mongo = '0.0.0.0'
        else:
            self.ip_mongo = '0.0.0.0'
        self.name_collection = os.getenv('MONGO_COLLECTION')
        self.user = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'root')
        self.user_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'root')
        self.port = os.getenv('MONGO_PORT', 27017)
        self.db = os.getenv('MONGO_INITDB_DATABASE')
        username = urllib.parse.quote_plus(self.user)
        password = urllib.parse.quote_plus(self.user_password)
        self.client = MongoClient('mongodb://%s:%s@%s:%s' % (username, password, self.ip_mongo, self.port))
        self.db = self.client[self.db]
        self.colection = self.db[str(self.name_collection)]

    def upload_json(self, filename, tags, additional_tags, extension):
        time_now = strftime("%Y-%m-%d %H:%M:%S", localtime())
        meta_mongo = {
            'file': filename,
            'tags': tags,
            'time': time_now,
            'user_tags': additional_tags,
            'extension': extension
        }
        return self.colection.insert_one(meta_mongo).inserted_id

    def get_all_files(self):
        cursor = self.colection.find({})
        result = []
        for item in cursor:
            result.append(item)
        return result
