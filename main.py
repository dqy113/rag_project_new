from langchain_chroma import Chroma
from zhipuai import ZhipuAI
from langchain.embeddings.base import Embeddings
import os
from dotenv import load_dotenv

# 加载.env里的智谱API密钥
load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

# 自定义智谱嵌入类，替代OpenAIEmbeddings
class ZhipuEmbedding(Embeddings):
    def __init__(self):
        self.client = ZhipuAI(api_key=ZHIPU_API_KEY)

    def embed_documents(self, texts):
        res = self.client.embeddings.create(input=texts, model="embedding-2")
        return [item.embedding for item in res.data]

    def embed_query(self, text):
        return self.embed_documents([text])[0]

# 向量库路径
PERSIST_DIR = "./chroma_db"
# 初始化智谱嵌入+向量库
embedding = ZhipuEmbedding()
vector_db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)

# 对外检索函数，rag.py导入用
def search_knowledge(query_str, top_k=5):
    relate_docs = vector_db.similarity_search(query_str, k=top_k)
    return relate_docs

# 本地测试
if __name__ == "__main__":
    print("===== 知识库检索测试 =====")
    query = "栈和队列有什么区别"
    relate_docs = search_knowledge(query, k=3)
    print(f"\n查询问题：{query}")
    for idx, doc in enumerate(relate_docs):
        print(f"\n【匹配内容{idx+1}】")
        print(doc.page_content)
        print(f"出处：{doc.metadata['source']} 第{doc.metadata.get('page', 0)}页")