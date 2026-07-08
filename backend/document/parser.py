# backend/document/parser.py


import re

from backend.models.document import Document

from backend.utils.logger import logger



class DocumentParser:
    """
    文档解析器

    负责:
    文本清洗
    格式规范化
    """


    def parse(
        self,
        document:Document
    )->Document:
        """
        清洗Document内容
        """


        logger.info(
            f"Parsing {document.filename}"
        )


        content = document.content


        content = self.clean_text(
            content
        )


        document.content = content


        return document



    def clean_text(
        self,
        text:str
    )->str:
        """
        文本清洗
        """


        # 删除多余空白

        text = re.sub(
            r"\s+",
            " ",
            text
        )


        # 删除特殊字符

        text = text.strip()


        return text