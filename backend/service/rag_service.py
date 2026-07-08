# backend/service/rag_service.py

import uuid
import time

from backend.utils.logger import logger

from backend.retrieval.retriever import Retriever
from backend.retrieval.prompt_builder import PromptBuilder

from backend.llm.llm_client import LLMClient

from backend.models.response import AnswerResponse


class RAGService:
    """
    RAG核心业务服务

    负责:
    question
        ↓
    retrieve
        ↓
    prompt build
        ↓
    LLM generate
        ↓
    response

    """

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient
    ):

        self.retriever = retriever

        self.prompt_builder = prompt_builder

        self.llm_client = llm_client



    def answer(
        self,
        question: str,
        history: str = ""
    ) -> AnswerResponse:


        trace_id = str(uuid.uuid4())[:8]

        start_time = time.time()


        logger.info(
            f"[{trace_id}] RAG流程开始"
        )

        logger.info(
            f"[{trace_id}] 用户问题: {question}"
        )


        try:

            # ======================
            # 1. Retriever检索
            # ======================

            logger.info(
                f"[{trace_id}] 开始知识检索"
            )


            chunks = self.retriever.search(
                question
            )


            logger.debug(
                f"[{trace_id}] "
                f"召回Chunk数量: {len(chunks)}"
            )


            for i, chunk in enumerate(chunks):

                logger.debug(
                    f"[{trace_id}] "
                    f"Chunk-{i}: "
                    f"{chunk.content[:100]}"
                )



            # ======================
            # 2. Prompt构建
            # ======================

            logger.info(
                f"[{trace_id}] 构建Prompt"
            )


            prompt = self.prompt_builder.build(
                question=question,
                history=history,
                chunks=chunks
            )


            logger.debug(
                f"[{trace_id}] Prompt长度:{len(prompt)}"
            )



            # ======================
            # 3. LLM生成
            # ======================

            logger.info(
                f"[{trace_id}] 调用大模型"
            )


            answer = self.llm_client.generate(
                prompt
            )



            # ======================
            # 4. 返回Response
            # ======================

            latency = (
                time.time()
                -
                start_time
            )


            references = []

            for chunk in chunks:

                references.append(
                    chunk.metadata.get(
                        "source",
                        "unknown"
                    )
                )


            logger.info(
                f"[{trace_id}] "
                f"RAG完成 "
                f"耗时:{latency:.2f}s"
            )


            return AnswerResponse(

                answer=answer,

                references=references,

                latency=latency

            )



        except Exception as e:


            latency = (
                time.time()
                -
                start_time
            )


            logger.error(
                f"[{trace_id}] "
                f"RAG异常:"
                f"{str(e)}"
            )


            return AnswerResponse(

                answer=
                "系统处理失败，请稍后重试",

                latency=latency,

                success=False,

                error_message=str(e)

            )