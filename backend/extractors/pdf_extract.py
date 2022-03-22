from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams,LTFigure,LTTextBox
from io import BytesIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfdocument import PDFDocument

import PyPDF2
class PDF():
    def pdf_to_text_file(self, path):
        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(path, 'rb')
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        filepath.close()
        device.close()
        retstr.close()
        return text

    def pdf_to_text_stream(self, stream):
        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        interpreter = PDFPageInterpreter(manager, device)
        for page in PDFPage.get_pages(stream, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        device.close()
        retstr.close()
        return text

    def pdf_to_text_stream_2(self,stream):
        parser = PDFParser(stream)
        doc = PDFDocument(parser)
        page = list(PDFPage.create_pages(doc))[0]
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        interpreter.process_page(page)
        layout = device.get_result()
        text = ""
        stack = []
        for obj in layout:
            if isinstance(obj, LTTextBox):
                text += obj.get_text()

            elif isinstance(obj, LTFigure):
                stack += list(obj)
        return text