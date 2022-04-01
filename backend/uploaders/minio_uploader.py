import io
import socket

import boto3
from minio import Minio
from minio.error import S3Error
import os


class minio_uploader():
    def __init__(self):
        self.name_bucket = os.getenv('MINIO_DEFAULT_BUCKETS')
        self.user = os.getenv('MINIO_ROOT_USER')
        self.user_password = os.getenv('MINIO_ROOT_PASSWORD')
        self.port = os.getenv('MINIO_PORT', 9000)
        self.isProd = bool(os.getenv('DEVELOPMENT_FLASK', True))
        if(self.isProd):
            try:
                self.ip_minio = socket.gethostbyname('minio_db')
            except:
                self.ip_minio = '0.0.0.0'
        else:
            self.ip_minio = '0.0.0.0'
        self.client = Minio(self.ip_minio + ":" + str(self.port), self.user, self.user_password, session_token=None, secure=False)
        self.s3 = boto3.resource('s3', endpoint_url='http://'+self.ip_minio+':'+str(self.port), aws_access_key_id=self.user,
                            aws_secret_access_key=self.user_password)
        #if not self.client.bucket_exists(self.name_bucket):
            #self.client.make_bucket(self.name_bucket)
        self.bucket = self.s3.Bucket(str(self.name_bucket))

    def upload_file(self, file):
        try:
            result = self.client.put_object(self.name_bucket, file.filename, file.stream,
                                            os.fstat(file.fileno()).st_size)
        except S3Error as exc:
            print("error to upload")
        # TODO:upload file
        return result

    def count_obj(self):
        objects = self.client.list_objects(self.name_bucket)
        i = 0
        for obj in objects:
            i = i + 1
        return i

    def get_file(self, filename):
        obj = self.client.get_object(self.name_bucket, filename)
        return obj

    def get_stream_file(self, filename):
        # TODO: create s3 object and move credentials to cfg file
        file_s3 = self.bucket.Object(filename)
        return io.BytesIO(file_s3.get()["Body"].read())

    def get_object(self):
        list_obj = []
        #self.bucket = self.s3.Bucket(self.name_bucket)
        for obj in self.bucket.objects.all():
            list_obj.append(obj.key)
        return list_obj
