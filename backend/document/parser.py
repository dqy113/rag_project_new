import re

from backend.models.document import Document
from backend.utils.logger import logger



class DocumentParser:


    def parse(
        self,
        document:Document
    )->Document:


        logger.info(
            f"Parsing {document.filename}"
        )


        document.content = self.clean_text(
            document.content
        )


        if "pages" in document.metadata:

            for page in document.metadata["pages"]:

                page["content"] = self.clean_text(
                    page["content"]
                )


        if "slides" in document.metadata:

            for slide in document.metadata["slides"]:

                slide["content"] = self.clean_text(
                    slide["content"]
                )


        if "paragraphs" in document.metadata:

            for paragraph in document.metadata["paragraphs"]:

                paragraph["content"] = self.clean_text(
                    paragraph["content"]
                )


        return document



    def clean_text(
        self,
        text:str
    )->str:


        text = re.sub(
            r"\s+",
            " ",
            text
        )


        return text.strip()