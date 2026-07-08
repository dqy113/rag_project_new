"""
Application Container

负责整个RAG系统的依赖注入和对象组装。

app.py 不直接创建任何service，
所有模块由这里统一初始化。
"""
from dotenv import load_dotenv
import os

load_dotenv()

print(
    "CONTAINER KEY:",
    os.getenv("ZHIPUAI_API_KEY")
)

# =========================
# VectorStore
# =========================

from backend.vectorstore.embedding import EmbeddingModel
from backend.vectorstore.chroma_manager import ChromaManager



# =========================
# Retrieval
# =========================

from backend.retrieval.retriever import Retriever
from backend.retrieval.prompt_builder import PromptBuilder



# =========================
# LLM
# =========================

from backend.llm.llm_client import LLMClient



# =========================
# Service
# =========================

from backend.service.rag_service import RAGService
from backend.service.conversation_service import ConversationService



# =========================
# Controller
# =========================

from backend.controller.chat_controller import ChatController



# ==================================================
# 1. 初始化 VectorStore 层
# ==================================================

embedding_model = EmbeddingModel()


chroma_manager = ChromaManager(
    persist_path="data/chroma_db",
    collection_name="knowledge_base"
)



# ==================================================
# 2. 初始化 Retrieval 层
# ==================================================

retriever = Retriever(
    embedding_model=embedding_model,
    chroma_manager=chroma_manager,
    top_k=5
)


prompt_builder = PromptBuilder()



# ==================================================
# 3. 初始化 LLM 层
# ==================================================

llm_client = LLMClient()



# ==================================================
# 4. 初始化 Service 层
# ==================================================

rag_service = RAGService(
    retriever=retriever,
    prompt_builder=prompt_builder,
    llm_client=llm_client
)


conversation_service = ConversationService()



# ==================================================
# 5. 初始化 Controller 层
# ==================================================

chat_controller = ChatController(
    rag_service=rag_service,
    conversation_service=conversation_service
)