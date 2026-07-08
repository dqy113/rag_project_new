"""
Metadata Manager

负责Document对象的持久化管理。

功能:
1. 保存Document
2. 查询Document
3. 删除Document
4. 更新状态
5. 更新标签

不负责:
- 文件读取
- PDF解析
- Embedding
- Chroma
"""


import json
import os

from typing import List, Optional

from backend.models.document import Document



class MetadataManager:


    def __init__(
        self,
        metadata_path="data/metadata/documents.json"
    ):

        self.metadata_path = metadata_path

        self._initialize()



    def _initialize(self):

        directory = os.path.dirname(
            self.metadata_path
        )


        if not os.path.exists(directory):

            os.makedirs(directory)


        # 文件不存在或者为空
        if (
            not os.path.exists(self.metadata_path)
            or os.path.getsize(self.metadata_path) == 0
        ):

            with open(
                self.metadata_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    ensure_ascii=False,
                    indent=4
                )



    def _document_to_dict(
        self,
        document:Document
    ):

        return {

            "document_id":
                document.document_id,

            "filename":
                document.filename,

            "filepath":
                document.filepath,

            "file_type":
                document.file_type,

            "course":
                document.course,

            "chapters":
                document.chapters,

            "tags":
                document.tags,

            "upload_time":
                document.upload_time,

            "status":
                document.status,

            "chunk_count":
                document.chunk_count

        }



    def _dict_to_document(
        self,
        data:dict
    ):

        return Document(

            document_id=data["document_id"],

            filename=data["filename"],

            filepath=data["filepath"],

            file_type=data["file_type"],

            course=data.get(
                "course",
                "default"
            ),

            chapters=data.get(
                "chapters",
                []
            ),

            tags=data.get(
                "tags",
                []
            ),

            upload_time=data.get(
                "upload_time"
            ),

            status=data.get(
                "status",
                "ready"
            ),

            chunk_count=data.get(
                "chunk_count",
                0
            )

        )



    def _load_documents(
        self
    ) -> List[Document]:


        with open(
            self.metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            data=json.load(file)


        return [

            self._dict_to_document(item)

            for item in data

        ]



    def _save_documents(
        self,
        documents:List[Document]
    ):


        data=[

            self._document_to_dict(doc)

            for doc in documents

        ]


        with open(
            self.metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )



    def add_document(
        self,
        document:Document
    ):

        documents=self._load_documents()


        documents.append(
            document
        )


        self._save_documents(
            documents
        )



    def get_all_documents(
        self
    )->List[Document]:

        return self._load_documents()



    def get_document(
        self,
        document_id:str
    )->Optional[Document]:

        documents=self._load_documents()


        for document in documents:

            if document.document_id == document_id:

                return document


        return None



    def delete_document(
        self,
        document_id:str
    )->bool:


        documents=self._load_documents()


        new_documents=[

            doc

            for doc in documents

            if doc.document_id != document_id

        ]


        if len(new_documents)==len(documents):

            return False


        self._save_documents(
            new_documents
        )


        return True



    def update_status(
        self,
        document_id:str,
        status:str
    ):


        documents=self._load_documents()


        for document in documents:

            if document.document_id == document_id:

                document.status=status


        self._save_documents(
            documents
        )



    def update_tags(
        self,
        document_id:str,
        tags:list[str]
    ):


        documents=self._load_documents()


        for document in documents:

            if document.document_id == document_id:

                document.tags=tags


        self._save_documents(
            documents
        )