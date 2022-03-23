from backend.nlp import natasha_parcer
from backend.extractors import docx_extract, pdf_extract
from backend.uploaders import minio_uploader, mongo_uploader


class back:
    def __init__(self):
        # TODO: cfg file
        self.minio = minio_uploader.minio_uploader("192.168.101.1", "9000", "pawa", "pawapawa", False)
        self.minio.set_bucket('pawa')
        self.mongo = mongo_uploader.mongo_uploader("192.168.101.1", "27017", "Pawa", "pawa")
        self.natasha = natasha_parcer.natasha_NLP()
        self.docx = docx_extract.doc_docx()
        self.pdf = pdf_extract.PDF()
        return
