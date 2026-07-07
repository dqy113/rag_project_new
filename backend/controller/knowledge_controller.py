from backend.service.knowledge_service import KnowledgeService

service = KnowledgeService()


def upload_document(uploaded_file):
    """
    上传文档接口
    """
    return service.upload_document(uploaded_file)


def delete_document(filename):
    """
    删除文档接口
    """
    return service.delete_document(filename)


def update_document(uploaded_file):
    """
    更新文档接口
    """
    return service.update_document(uploaded_file)


def get_document_list():
    """
    获取知识库文档列表
    """
    return service.get_document_list()


def rebuild_database():
    """
    重建知识库（可选）
    """
    return service.rebuild_database()