# backend/rag.py
import uuid
import time
from backend.utils.logger import logger
from backend.service.rag_service import RAGService


def ask(user_question: str) -> str:
    """
    【中转枢纽】完美对接原本的 app.py，不让前端改一行代码。
    同时在这里开启全链路日志摄像头。
    """
    trace_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    logger.info(f"================ [RAG 流程开始] ID: {trace_id} ================")
    logger.info(f"[{trace_id}] 【前端大入口】收到用户提问: '{user_question}'")

    try:
        # 实例化并调用新分类的服务层
        rag_service = RAGService()
        response_obj = rag_service.ask(user_question, trace_id=trace_id)

        latency = time.time() - start_time

        if response_obj.success:
            logger.info(f"[{trace_id}] 【前端大入口】流程成功结束，总耗时: {latency:.2f}s")
            # 如果有引用来源，顺便在日志里记一下
            if response_obj.references:
                logger.info(f"[{trace_id}] 本次回答知识来源于: {', '.join(response_obj.references)}")
            return response_obj.answer
        else:
            logger.error(f"[{trace_id}] 【前端大入口】后端报错: {response_obj.error_message}")
            return f"【回答失败】: {response_obj.error_message}"

    except Exception as e:
        latency = time.time() - start_time
        logger.exception(f"[{trace_id}] 【前端大入口】系统致命崩溃")
        return f"【系统错误】后端调用失败，原因: {str(e)}"