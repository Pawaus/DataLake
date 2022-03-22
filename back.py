from backend.nlp import natasha_parcer
from backend.extractors import docx_extract, pdf_extract
from backend.uploaders import minio_uploader, mongo_uploader

class back:
    def __init__(self):
        self.minio = minio_uploader.minio_uploader("localhost", "9000", "pawa", "pawapawa", False)
        self.minio.set_bucket('pawa')
        self.mongo = mongo_uploader.mongo_uploader("localhost", "27017", "Pawa", "pawa")
        self.natasha = natasha_parcer.natasha_NLP()
        self.docx = docx_extract.doc_docx()
        self.pdf = pdf_extract.PDF()
        return