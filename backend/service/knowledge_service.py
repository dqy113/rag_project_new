import os

from backend.document.loader import load_document
from backend.document.splitter import split_text
from backend.vectorstore.embedding import (
    add_chunks,
    delete_document as delete_vector_document,
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
        """
        上传新文档
        如果存在同名文档，则自动更新
        """

        save_path = os.path.join(self.data_dir, uploaded_file.name)

        # 如果存在同名文件，先删除旧知识库
        if os.path.exists(save_path):
            self.delete_document(uploaded_file.name)

        # 保存文件
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 读取文档
        docs = load_document(save_path)

        # 文本切块
        chunks = split_text(docs)

        # 写入向量数据库
        add_chunks(chunks)

        return {
            "success": True,
            "message": "文档上传成功"
        }

    # ==========================
    # 删除文档
    # ==========================
    def delete_document(self, filename):
        """
        删除知识库中的文档
        包括：
        1. Chroma中的向量
        2. data目录中的原文件
        """

        try:
            # 删除向量
            delete_vector_document(filename)

            # 删除本地文件
            file_path = os.path.join(self.data_dir, filename)

            if os.path.exists(file_path):
                os.remove(file_path)

            return {
                "success": True,
                "message": "删除成功"
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }

    # ==========================
    # 更新文档
    # ==========================
    def update_document(self, uploaded_file):
        """
        更新知识库
        实际采用：
        删除旧文档
        +
        重新上传
        """

        self.delete_document(uploaded_file.name)

        return self.upload_document(uploaded_file)

    # ==========================
    # 获取知识库所有文件
    # ==========================
    def get_document_list(self):

        return list_documents()

    # ==========================
    # 重建知识库（可选）
    # ==========================
    def rebuild_database(self):
        """
        扫描data目录
        重新构建整个知识库
        """

        files = os.listdir(self.data_dir)

        for file in files:

            file_path = os.path.join(self.data_dir, file)

            docs = load_document(file_path)

            chunks = split_text(docs)

            add_chunks(chunks)

        return {
            "success": True,
            "message": "知识库重建完成"
        }