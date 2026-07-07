# backend/service/rag_service.py
import uuid
import time
from backend.utils.logger import logger
from backend.llm.llm_client import ZhipuLLMClient


class RAGService:
    def __init__(self):
        self.llm_client = ZhipuLLMClient()
        # self.retriever = ... (这里对接你 backend/retrieval/retriever.py 的实例化对象)

    def answer_question(self, user_query: str) -> str:
        """
        RAG 核心服务：检索 -> 组装 -> 智谱生成
        """
        # 1. 每次用户提问，生成唯一的全链路跟踪 ID (取前 8 位即可)
        trace_id = str(uuid.uuid4())[:8]

        logger.info(f"======== [RAG 流程开始] Trace ID: {trace_id} ========")
        logger.info(f"[{trace_id}] 用户原始提问: '{user_query}'")

        start_time = time.time()

        try:
            # 2. 模拟知识库检索阶段 (这里你应该替换为调用你的 retriever.py)
            logger.info(f"[{trace_id}] 正在检索 Chroma 向量数据库...")
            time.sleep(0.2)  # 模拟向量检索耗时

            # 假装这是从你的 data/chroma_db 中检索出来的 Top-K 文档
            mock_retrieved_docs = [
                {"source": "company_policy.pdf", "score": 0.88, "text": "智谱AI大模型工程日志的规范要求使用Loguru库。"},
                {"source": "developer_guide.txt", "score": 0.72,
                 "text": "RAG系统检索到的上下文必须在DEBUG级别记录，防止INFO日志过大。"}
            ]

            # 在 DEBUG 级别中详细记录检索出来的参考文档
            logger.debug(f"[{trace_id}] 向量数据库检索完成，成功召回 {len(mock_retrieved_docs)} 条上下文片段.")
            for i, doc in enumerate(mock_retrieved_docs):
                logger.debug(
                    f"    - [文档 {i + 1}] 来源: {doc['source']}, 相似度得分: {doc['score']}, 内容: {doc['text']}")

            # 3. 提示词组装阶段 (把检索内容和用户问题拼起来)
            context_str = "\n".join([doc["text"] for doc in mock_retrieved_docs])
            final_prompt = f"请结合以下参考资料回答用户的问题。\n\n【参考资料】：\n{context_str}\n\n【用户问题】：\n{user_query}"

            # 4. 调用智谱 LLM 阶段
            system_prompt = "你是一个基于专属知识库回答问题的 AI 助手，请严格根据参考资料回答，不要胡编乱造。"
            llm_response = self.llm_client.chat_completion(
                prompt=final_prompt,
                system_prompt=system_prompt,
                model="glm-4",
                trace_id=trace_id
            )

            # 5. 流程结束统计
            total_latency = time.time() - start_time
            logger.info(f"[{trace_id}] RAG 全链路执行成功，总耗时: {total_latency:.2f} 秒.")
            logger.info(f"======== [RAG 流程结束] Trace ID: {trace_id} ========")

            return llm_response

        except Exception as e:
            total_latency = time.time() - start_time
            logger.error(f"[{trace_id}] RAG 全链路异常中断！当前环节耗时: {total_latency:.2f} 秒.")
            logger.info(f"======== [RAG 流程异常结束] Trace ID: {trace_id} ========")
            return "抱歉，系统处理您的请求时出现异常，请稍后再试。"