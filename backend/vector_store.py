# backend/vector_store.py
import os
from langchain_chroma import Chroma
from zhipuai import ZhipuAI

# 从系统的环境变量或者直接从 .env 自动读取
API_KEY = os.getenv("ZHIPU_API_KEY")

# 初始化智谱客户端（用于生成向量）
client = ZhipuAI(api_key=API_KEY)

# 队友写好的智谱向量嵌入类，原封不动搬过来
class ZhipuEmb:
    def embed_documents(self, texts):
        vecs = []
        for txt in texts:
            resp = client.embeddings.create(model="embedding-2", input=txt)
            vecs.append(resp.data[0].embedding)
        return vecs

    def embed_query(self, text):
        return self.embed_documents([text])[0]

# 实例化向量嵌入模型
emb = ZhipuEmb()

# 本地数据库存储路径 (注意：因为在backend目录下执行，路径可能需要返回上一级)
PERSIST_DIR = "./chroma_db"

def search_relevant_docs(query: str, k: int = 3) -> str:
    """
    根据用户的问题，去本地的 Chroma 知识库里捞取最相关的文本
    """
    if not os.path.exists(PERSIST_DIR):
        return "【系统提示】本地暂未检测到本地向量库，请先运行 main.py 生成 ./chroma_db 文件夹。"
    
    # 1. 直接加载本地的向量数据库
    vector_db = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
    
    # 2. 检索前 k 个最相关的知识片段
    relate_docs = vector_db.similarity_search(query, k=k)
    
    # 3. 把捞出来的片段拼接成一大段文本，喂给大模型做参考
    context_list = []
    for idx, doc in enumerate(relate_docs):
        source = doc.metadata.get('source_file', '未知文件')
        page = doc.metadata.get('page_num', '未知页码')
        context_list.append(f"[参考片段{idx+1} (来源: {source} 第{page}页)]:\n{doc.page_content}")
        
    return "\n\n".join(context_list)