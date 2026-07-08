"""
Knowledge Controller

知识库管理控制层

职责:

1. 接收前端知识库请求
2. 调用KnowledgeService
3. 返回处理结果


不负责:

- 文档解析
- 向量处理
- 数据存储
"""


from backend.service.knowledge_service import KnowledgeService



class KnowledgeController:


    def __init__(
        self,
        knowledge_service:KnowledgeService
    ):

        self.knowledge_service = knowledge_service



    def upload_document(
        self,
        file_path:str,
        course:str="default",
        tags:list[str]=None
    ):
        """
        上传知识文档


        输入:

            file_path:
                文件路径


            course:
                课程


            tags:
                标签


        输出:

            Document
        """


        document = (
            self.knowledge_service
            .add_document(
                file_path=file_path,
                course=course,
                tags=tags
            )
        )


        return document



    def delete_document(
        self,
        document_id:str
    ):
        """
        删除知识文档


        输入:

            document_id


        输出:

            bool

        """


        result = (
            self.knowledge_service
            .delete_document(
                document_id
            )
        )


        return result



    def get_documents(
        self
    ):
        """
        获取知识库列表


        用于:

        - 前端展示
        - 文件管理页面

        """


        documents = (
            self.knowledge_service
            .get_documents()
        )


        return documents



    def get_document(
        self,
        document_id:str
    ):
        """
        获取指定文档信息
        """


        document = (
            self.knowledge_service
            .get_document(
                document_id
            )
        )


        return document