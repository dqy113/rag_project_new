"""
Knowledge Service

知识库管理核心服务

职责:
1. 添加知识文档
2. 删除知识文档
3. 查询知识库文档


负责协调:

Document
    ↓
Chunk
    ↓
Vector Database


不负责:
- 文件解析
- embedding实现
- Chroma实现
"""


from backend.models.document import Document



class KnowledgeService:


    def __init__(
        self,
        loader,
        parser,
        splitter,
        embedding_model,
        chroma_manager,
        metadata_manager
    ):
        """
        初始化知识库服务

        所有依赖由container注入
        """

        self.loader = loader

        self.parser = parser

        self.splitter = splitter

        self.embedding_model = embedding_model

        self.chroma_manager = chroma_manager

        self.metadata_manager = metadata_manager



    def add_document(
        self,
        file_path:str,
        course:str="default",
        tags:list[str]=None
    )->Document:
        """
        添加知识文档


        输入:

            file_path:
                文件路径


            course:
                所属课程


            tags:
                文档标签



        输出:

            Document对象



        流程:

            文件

            ↓

            DocumentLoader

            ↓

            Parser

            ↓

            Splitter

            ↓

            Embedding

            ↓

            Chroma

            ↓

            Metadata

        """


        if tags is None:

            tags=[]



        # =====================
        # 1. 加载文件
        # =====================

        document = self.loader.load(
            file_path
        )



        # 设置业务信息

        document.course = course

        document.tags = tags

        document.status = "processing"



        # =====================
        # 2. 文本预处理
        # =====================

        document = self.parser.parse(
            document
        )



        # =====================
        # 3. 文档切块
        # =====================

        chunks = self.splitter.split(
            document
        )



        # =====================
        # 4. 生成embedding
        # =====================

        texts = [

            chunk.content

            for chunk in chunks

        ]


        vectors = (
            self.embedding_model
            .embed_documents(
                texts
            )
        )



        # =====================
        # 5. 更新Chunk信息
        # =====================

        for chunk, vector in zip(
            chunks,
            vectors
        ):

            chunk.embedding = vector


            chunk.metadata.update(
                {

                    "document_id":
                    document.document_id,


                    "course":
                    document.course,


                    "tags":
                    document.tags

                }
            )



        # =====================
        # 6. 写入Chroma
        # =====================

        self.chroma_manager.add_chunks(
            chunks
        )



        # =====================
        # 7. 保存文档信息
        # =====================

        document.chunk_count = len(
            chunks
        )

        document.status = "ready"



        self.metadata_manager.add_document(
            document
        )


        return document



    def delete_document(
        self,
        document_id:str
    )->bool:
        """
        删除知识文档


        流程:

            document_id

            ↓

            Chroma删除Chunk

            ↓

            metadata删除Document

        """


        document = (
            self.metadata_manager
            .get_document(
                document_id
            )
        )


        if document is None:

            return False



        # 删除向量数据

        self.chroma_manager.delete_by_document_id(
            document_id
        )



        # 删除文档记录

        self.metadata_manager.delete_document(
            document_id
        )


        return True



    def get_documents(
        self
    )->list[Document]:
        """
        获取知识库全部文档

        用于前端展示
        """

        return (
            self.metadata_manager
            .get_all_documents()
        )



    def get_document(
        self,
        document_id:str
    ):
        """
        获取单个文档
        """

        return (
            self.metadata_manager
            .get_document(
                document_id
            )
        )