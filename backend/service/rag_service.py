# backend/service/rag_service.py
import time
from backend.utils.logger import logger
from backend.llm.llm_client import ZhipuLLMClient
from backend.retrieval.retriever import KnowledgeRetriever
from backend.models.response import AnswerResponse


class RAGService:
    def __init__(self):
        self.llm_client = ZhipuLLMClient()
        self.retriever = KnowledgeRetriever()

    def ask(self, user_question: str, trace_id: str = "SYSTEM") -> AnswerResponse:
        """核心业务逻辑处理"""
        start_time = time.time()
        logger.info(f"[{trace_id}] 【服务层】开始调度核心业务逻辑...")

        try:
            # 1. 调度检索层（传递身份证 trace_id）
            docs = self.retriever.search_knowledge(user_question, top_k=3, trace_id=trace_id)

            # 2. 提取并清洗知识引用
            context_list = []
            references = []
            for idx, doc in enumerate(docs):
                source = doc.metadata.get('source', '未知文件')
                page = doc.metadata.get('page', '未知页码')
                ref_str = f"{source} 第{page}页"
                references.append(ref_str)

                # 在 DEBUG 日志记录内容预览，防止正常运行时刷屏
                logger.debug(f"[{trace_id}] 【服务层】参考片段预览: {doc.page_content[:30]}...")
                context_list.append(f"[参考片段{idx + 1} (来源: {ref_str})]:\n{doc.page_content}")

            context = "\n\n".join(context_list)

            # 3. 组装 RAG 提示词
            rag_prompt = f"""你是一个专业的数据结构智能助教。请严格根据以下给出的【已知知识库信息】来回答用户的【问题】。

【回答规则】：
1. 严格依据下面的知识库内容回答，禁止编造不存在的信息；
2. 涉及算法时间/空间复杂度等数学表达式时，必须使用标准Markdown公式格式：所有复杂度公式前后用 $ 符号包裹；
3. 术语不能混淆；
4. 如果已知信息里无法回答该问题，请礼貌地回答你不知道，不要瞎编。

【已知知识库信息】：
{context}

【用户的实际问题】：
{user_question}
"""

            # 4. 调用大模型
            final_answer = self.llm_client.get_llm_response(rag_prompt, trace_id=trace_id)

            return AnswerResponse(
                answer=final_answer,
                references=list(set(references)),
                latency=round(time.time() - start_time, 2),
                success=True
            )

        except Exception as e:
            logger.exception(f"[{trace_id}] 【服务层】内部处理发生未知异常")
            return AnswerResponse(
                answer="系统处理失败",
                latency=round(time.time() - start_time, 2),
                success=False,
                error_message=str(e)
            )