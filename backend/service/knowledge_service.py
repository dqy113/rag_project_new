import os

from backend.document.loader import load_document
from backend.document.splitter import split_text

from backend.vectorstore.embedding import (
    add_chunks,
    delete_document,
    list_documents
)


class KnowledgeService:

    def __init__(self):
        self.data_dir = "data"

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    # ==========================
    # 上传文档
    # ==========================
    def upload_document(self, uploaded_file):

        save_path = os.path.join(
            self.data_dir,
            uploaded_file.name
        )

        # 保存文件
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 读取文档
        docs = load_document(save_path)

        # 分块
        chunks = split_text(docs)

        # 向量化
        add_chunks(chunks)

        return True

    # ==========================
    # 删除文档
    # ==========================
    def delete_document(self, filename):

        # 删除向量库
        delete_document(filename)

        # 删除原文件
        file_path = os.path.join(
            self.data_dir,
            filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        return True

    # ==========================
    # 更新文档
    # ==========================
    def update_document(self, uploaded_file):

        self.delete_document(uploaded_file.name)

        self.upload_document(uploaded_file)

        return True

    # ==========================
    # 获取知识库所有文档
    # ==========================
    def list_documents(self):

        return list_documents()