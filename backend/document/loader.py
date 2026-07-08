import os

from backend.models.document import Document
from backend.utils.logger import logger


class DocumentLoader:

    def __init__(self):
        pass


    def load(
        self,
        file_path:str
    ) -> Document:

        suffix = os.path.splitext(file_path)[1].lower()


        if suffix == ".pdf":
            return self.load_pdf(file_path)

        elif suffix == ".txt":
            return self.load_txt(file_path)

        elif suffix == ".docx":
            return self.load_docx(file_path)

        elif suffix == ".pptx":
            return self.load_pptx(file_path)

        else:
            raise ValueError(
                f"Unsupported file type:{suffix}"
            )


    def load_pdf(
        self,
        file_path:str
    ) -> Document:

        from pypdf import PdfReader


        reader = PdfReader(file_path)


        pages = []

        texts = []


        for index, page in enumerate(reader.pages):

            text = page.extract_text() or ""


            texts.append(text)


            pages.append(
                {
                    "page": index + 1,
                    "content": text
                }
            )


        content = "\n".join(texts)


        return Document(

            id=os.path.basename(file_path),

            filename=os.path.basename(file_path),

            content=content,

            metadata={
                "source":file_path,
                "type":"pdf",
                "pages":pages
            },

            file_type="pdf"

        )



    def load_txt(
        self,
        file_path:str
    ) -> Document:


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content=f.read()


        return Document(

            id=os.path.basename(file_path),

            filename=os.path.basename(file_path),

            content=content,

            metadata={
                "source":file_path,
                "type":"txt"
            },

            file_type="txt"

        )



    def load_docx(
        self,
        file_path:str
    ) -> Document:


        from docx import Document as DocxDocument


        doc = DocxDocument(file_path)


        paragraphs=[]


        for index,p in enumerate(doc.paragraphs):

            paragraphs.append(
                {
                    "paragraph":index+1,
                    "content":p.text
                }
            )


        content="\n".join(
            [
                p["content"]
                for p in paragraphs
            ]
        )


        return Document(

            id=os.path.basename(file_path),

            filename=os.path.basename(file_path),

            content=content,

            metadata={
                "source":file_path,
                "type":"docx",
                "paragraphs":paragraphs
            },

            file_type="docx"

        )



    def load_pptx(
        self,
        file_path:str
    ) -> Document:


        from pptx import Presentation


        prs = Presentation(file_path)


        slides=[]


        texts=[]


        for index,slide in enumerate(prs.slides):

            slide_text=[]


            for shape in slide.shapes:

                if hasattr(shape,"text"):

                    slide_text.append(
                        shape.text
                    )


            text="\n".join(slide_text)


            texts.append(text)


            slides.append(
                {
                    "slide":index+1,
                    "content":text
                }
            )


        content="\n".join(texts)


        return Document(

            id=os.path.basename(file_path),

            filename=os.path.basename(file_path),

            content=content,

            metadata={
                "source":file_path,
                "type":"pptx",
                "slides":slides
            },

            file_type="pptx"

        )