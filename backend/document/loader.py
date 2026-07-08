import os
import uuid

from backend.models.document import Document
from backend.utils.logger import logger



class DocumentLoader:
    """
    文档加载器

    支持:
    PDF
    TXT
    DOCX
    PPTX

    输入:
        文件路径

    输出:
        Document对象
    """



    def __init__(self):
        pass



    def load(
        self,
        file_path:str
    )->Document:
        """
        根据文件类型选择加载方式
        """

        suffix = (
            os.path.splitext(file_path)[1]
            .lower()
        )


        if suffix == ".pdf":

            return self.load_pdf(
                file_path
            )


        elif suffix == ".txt":

            return self.load_txt(
                file_path
            )


        elif suffix == ".docx":

            return self.load_docx(
                file_path
            )


        elif suffix == ".pptx":

            return self.load_pptx(
                file_path
            )


        else:

            raise ValueError(
                f"Unsupported file type:{suffix}"
            )



    def create_document(
        self,
        file_path:str,
        content:str,
        file_type:str
    )->Document:
        """
        创建统一Document对象

        所有格式最后都会经过这里
        """

        return Document(

            document_id=str(
                uuid.uuid4()
            ),

            filename=os.path.basename(
                file_path
            ),

            filepath=file_path,

            file_type=file_type,


            # 文档正文
            content=content,


            # 原始信息
            metadata={

                "source":file_path,

                "type":file_type

            }

        )



    def load_pdf(
        self,
        file_path:str
    )->Document:

        from pypdf import PdfReader


        reader = PdfReader(
            file_path
        )


        texts=[]


        for page in reader.pages:

            text = (
                page.extract_text()
                or ""
            )

            texts.append(
                text
            )


        content="\n".join(
            texts
        )


        return self.create_document(

            file_path,

            content,

            "pdf"

        )



    def load_txt(
        self,
        file_path:str
    )->Document:


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content=f.read()



        return self.create_document(

            file_path,

            content,

            "txt"

        )



    def load_docx(
        self,
        file_path:str
    )->Document:


        from docx import Document as DocxDocument


        doc = DocxDocument(
            file_path
        )


        texts=[]


        for paragraph in doc.paragraphs:

            texts.append(
                paragraph.text
            )


        content="\n".join(
            texts
        )


        return self.create_document(

            file_path,

            content,

            "docx"

        )



    def load_pptx(
        self,
        file_path:str
    )->Document:


        from pptx import Presentation


        prs = Presentation(
            file_path
        )


        texts=[]


        for slide in prs.slides:

            for shape in slide.shapes:

                if hasattr(
                    shape,
                    "text"
                ):

                    texts.append(
                        shape.text
                    )


        content="\n".join(
            texts
        )


        return self.create_document(

            file_path,

            content,

            "pptx"

        )