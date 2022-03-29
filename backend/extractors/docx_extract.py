import docx
import io
import docx2txt


class doc_docx():
    def load_text(self, stream):
        doc = docx.Document(stream)
        fullText = ""
        for para in doc.paragraphs:
            fullText += " " + para.text
        return fullText

    def load_txt(self, stream):
        doc = docx2txt.process(stream)
        return doc
