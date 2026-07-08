from backend.utils.logger import logger
# backend/retrieval/retriever.py

from backend.vectorstore.embedding import EmbeddingModel
from backend.vectorstore.chroma_manager import ChromaManager

from backend.models.chunk import Chunk


class Retriever:
    """
    RAG知识检索模块。

    负责将用户问题转换为向量，
    在向量数据库中进行相似度搜索，
    返回最相关的知识Chunk。

    不负责:
    - Prompt生成
    - LLM调用
    - 答案生成
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        chroma_manager: ChromaManager,
        top_k: int = 5
    ):
        """
        初始化Retriever。

        输入:

            embedding_model:
                文本向量化模型

            chroma_manager:
                向量数据库管理器

            top_k:
                返回前K个结果
        """

        self.embedding_model = embedding_model

        self.chroma_manager = chroma_manager

        self.top_k = top_k



    def search(
        self,
        question: str
    ) -> list[Chunk]:
        """
        检索入口函数。

        完整流程:

        question

        →

        Embedding

        →

        Vector Search

        →

        Top-K Chunk


        输入:

            question:
                用户问题


        输出:

            list[Chunk]
                最相关知识片段
        """


        # 1. 问题向量化
        query_vector = (
            self.embedding_model
            .embed_query(question)
        )


        # 2. 向量数据库检索
        chunks = (
            self.chroma_manager
            .similarity_search(
                query_vector,
                self.top_k
            )
        )


        return chunks



    def similarity_search(
        self,
        question: str
    ) -> list[Chunk]:
        """
        执行语义相似度搜索。


        输入:

            question:str


        输出:

            list[Chunk]


        说明:

            这是search内部调用函数，
            用于封装底层检索逻辑。
        """


        vector = (
            self.embedding_model
            .embed_query(question)
        )


        return (
            self.chroma_manager
            .similarity_search(
                vector,
                self.top_k
            )
        )



    def update_top_k(
        self,
        top_k:int
    ):
        """
        动态修改检索数量。


        输入:

            top_k:int


        输出:

            None


        示例:

            top_k=3

            返回3个Chunk

        """

        self.top_k = top_k