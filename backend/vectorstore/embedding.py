# backend/vectorstore/embedding.py

from sentence_transformers import SentenceTransformer
from backend.utils.logger import logger


class EmbeddingModel:
    """
    Embedding模型封装

    text -> vector

    用于:
    1. 文档Chunk向量化
    2. 用户问题向量化
    """

    def __init__(
        self,
        model_name="BAAI/bge-small-zh-v1.5"
    ):

        self.model_name = model_name

        logger.info(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

        logger.info(
            "Embedding model loaded"
        )


    def embed_text(
        self,
        text: str
    ) -> list[float]:
        """
        单文本embedding

        输入:
            text

        输出:
            vector
        """

        vector = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return vector.tolist()



    def embed_documents(
        self,
        texts:list[str]
    ) -> list[list[float]]:
        """
        批量文本embedding

        用于知识库构建
        """

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return vectors.tolist()



    def embed_query(
        self,
        query:str
    ) -> list[float]:
        """
        用户问题embedding

        和embed_text保持一致

        单独写方便Retriever调用
        """

        return self.embed_text(query)