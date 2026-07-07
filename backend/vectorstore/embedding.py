import os
from dotenv import load_dotenv

from zhipuai import ZhipuAI

from langchain.embeddings.base import Embeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()


# ==========================
# 智谱 Embedding
# ==========================
class ZhipuEmbedding(Embeddings):

    def __init__(self):
        self.client = ZhipuAI(
            api_key=os.getenv("ZHIPUAI_API_KEY")
        )

    def embed_documents(self, texts):
        response = self.client.embeddings.create(
            model="embedding-2",
            input=texts
        )

        return [item.embedding for item in response.data]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


# ==========================
# 初始化向量数据库
# ==========================

embedding = ZhipuEmbedding()

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)


# ==========================
# 添加文档
# ==========================

def add_chunks(chunks):
    """
    chunks:
    [
        {
            "text":"......",
            "source_file":"xx.pdf",
            "page_num":1
        }
    ]
    """

    docs = []

    for chunk in chunks:

        docs.append(
            Document(
                page_content=chunk["text"],
                metadata={
                    "source": chunk["source_file"],
                    "page": chunk["page_num"]
                }
            )
        )

    vector_db.add_documents(docs)


# ==========================
# 相似度检索
# ==========================

def search_knowledge(query, top_k=5):

    return vector_db.similarity_search(
        query,
        k=top_k
    )


# ==========================
# 删除某个文件
# ==========================

def delete_document(filename):

    collection = vector_db._collection

    result = collection.get(
        where={
            "source": filename
        }
    )

    ids = result["ids"]

    if len(ids) > 0:
        collection.delete(ids=ids)


# ==========================
# 获取所有文档
# ==========================

def list_documents():

    collection = vector_db._collection

    result = collection.get()

    files = set()

    for meta in result["metadatas"]:
        files.add(meta["source"])

    return list(files)