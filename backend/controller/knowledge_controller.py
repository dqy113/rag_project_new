from backend.service.knowledge_service import KnowledgeService


class KnowledgeController:

    def __init__(self):
        self.service = KnowledgeService()

    # ==========================
    # 上传文档
    # ==========================
    def upload_document(self, uploaded_file):
        return self.service.upload_document(uploaded_file)

    # ==========================
    # 删除文档
    # ==========================
    def delete_document(self, filename):
        return self.service.delete_document(filename)

    # ==========================
    # 更新文档
    # ==========================
    def update_document(self, uploaded_file):
        return self.service.update_document(uploaded_file)

    # ==========================
    # 获取知识库文件列表
    # ==========================
    def get_document_list(self):
        return self.service.get_document_list()

    # ==========================
    # 重建知识库
    # ==========================
    def rebuild_database(self):
        return self.service.rebuild_database()