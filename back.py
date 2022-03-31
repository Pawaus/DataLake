from backend.nlp import natasha_parcer
from backend.extractors import docx_extract, pdf_extract
from backend.uploaders import minio_uploader, mongo_uploader
import socket


class back:
    def __init__(self):
        # TODO: cfg file
        ip_minio = ''
        ip_mongo = ''
        try:
            ip_minio = socket.gethostbyname('minio_db')
            ip_mongo = socket.gethostbyname('mongo_db')
        except:
            ip_minio = '0.0.0.0'
            ip_mongo = '0.0.0.0'
        print(ip_mongo)
        print(ip_minio)
        self.minio = minio_uploader.minio_uploader(ip_minio, "9000", "pawa", "pawapawa", False)
        self.minio.set_bucket("pawa")
        self.mongo = mongo_uploader.mongo_uploader(ip_mongo, "27017", 'root', 'root', "Pawa", "pawa")
        self.natasha = natasha_parcer.natasha_NLP()
        self.docx = docx_extract.doc_docx()
        self.pdf = pdf_extract.PDF()
        return
