# backend/retrieval/retriever.py
import os
from langchain_chroma import Chroma
from zhipuai import ZhipuAI
from langchain.embeddings.base import Embeddings
from backend.utils.logger import logger


class ZhipuEmbedding(Embeddings):
    def __init__(self):
        # 兼容队友的 .env 读取
        api_key = os.getenv("ZHIPU_API_KEY")
        self.client = ZhipuAI(api_key=api_key)

    def embed_documents(self, texts):
        res = self.client.embeddings.create(input=texts, model="embedding-2")
        return [item.embedding for item in res.data]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


class KnowledgeRetriever:
    def __init__(self):
        self.persist_dir = "./chroma_db"
        self.embedding = ZhipuEmbedding()

    def search_knowledge(self, query_str: str, top_k: int = 3, trace_id: str = "SYSTEM") -> list:
        """前往 Chroma 数据库实施匹配检索"""
        if not os.path.exists(self.persist_dir):
            logger.warning(f"[{trace_id}] 【检索层】未检测到本地向量库，路径不存在: {self.persist_dir}")
            return []

        logger.info(f"[{trace_id}] 【检索层】正在向 Chroma 库发起向量检索, 关键词: '{query_str}'")
        try:
            vector_db = Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding)
            relate_docs = vector_db.similarity_search(query_str, k=top_k)
            logger.info(f"[{trace_id}] 【检索层】检索匹配成功，成功召回 {len(relate_docs)} 条参考片段。")
            return relate_docs
        except Exception as e:
            logger.exception(f"[{trace_id}] 【检索层】Chroma 数据库检索发生崩溃")
            return []