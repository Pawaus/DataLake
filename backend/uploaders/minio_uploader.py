import io

import boto3
from minio import Minio
from minio.error import S3Error
import os


class minio_uploader():
    def __init__(self, ip, port, user, passwd, security):
        self.name_bucket = ""
        self.client = Minio(ip + ":" + port, user, passwd, session_token=None, secure=security)
        self.s3 = boto3.resource('s3', endpoint_url='http://'+ip+':'+port, aws_access_key_id='3GYPMFGY6DLUVJF8DN5R',
                            aws_secret_access_key='UN9GVBDJg6BhdmBxrYGgjfs+KsGGC++R1aHs3IgW')


    def set_bucket(self, bucket):
        self.name_bucket = bucket
        self.bucket = self.s3.Bucket(str(self.name_bucket))
        if not self.client.bucket_exists(self.name_bucket):
            self.client.make_bucket(self.name_bucket)

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
        # TODO:return list objects
        list_obj = []
        self.bucket = self.s3.Bucket(self.name_bucket)
        for obj in self.bucket.objects.all():
            list_obj.append(obj.key)
        return list_obj
