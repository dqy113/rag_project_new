# backend/service/rag_service.py

<<<<<<< Updated upstream
from backend.retrieval.retriever import Retriever
from backend.retrieval.prompt_builder import PromptBuilder
from backend.llm.llm_client import LLMClient

from backend.models.response import AnswerResponse
from backend.models.chunk import Chunk
=======
import uuid
import time

from backend.utils.logger import logger

from backend.retrieval.retriever import Retriever
from backend.retrieval.prompt_builder import PromptBuilder

from backend.llm.llm_client import LLMClient

from backend.models.response import AnswerResponse
>>>>>>> Stashed changes


class RAGService:
    """
<<<<<<< Updated upstream
    RAG核心业务服务。

    负责协调:
    1. 用户问题处理
    2. 知识检索
    3. Prompt构建
    4. 大模型生成
    5. 返回标准答案

    本类不负责具体实现，
    只负责业务流程编排。
    """

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient
    ):
        """
        初始化RAG服务。

        输入:
            retriever:
                知识检索模块

            prompt_builder:
                Prompt生成模块

            llm_client:
                大模型调用模块
        """

        self.retriever = retriever

        self.prompt_builder = prompt_builder

        self.llm_client = llm_client



    def answer(
        self,
        question: str,
        history: str = ""
    ) -> AnswerResponse:
        """
        RAG完整问答流程入口。

        流程:

        question
            ↓
        retrieve
            ↓
        chunks
            ↓
        build prompt
            ↓
        LLM generate
            ↓
        AnswerResponse


        输入:
            question:
                用户问题

            history:
                历史聊天上下文


        输出:
            AnswerResponse
        """


        # 1. 检索相关知识
        chunks = self.retrieve(
            question
        )


        # 2. 构造Prompt
        prompt = self.build_prompt(
            question,
            history,
            chunks
        )


        # 3. 调用大模型
        answer = self.generate(
            prompt
        )


        # 4. 提取引用
        references = self.extract_references(
            chunks
        )


        # 5. 返回统一格式
        return AnswerResponse(
            answer=answer,
            references=references
        )



    def retrieve(
        self,
        question: str
    ) -> list[Chunk]:
        """
        根据问题检索相关知识。


        输入:
            question:str


        输出:
            list[Chunk]


        调用:

        question

        →

        Embedding

        →

        Chroma Search

        →

        TopK Chunk
        """


        return self.retriever.search(
            question
        )



    def build_prompt(
        self,
        question: str,
        history: str,
        chunks: list[Chunk]
    ) -> str:
        """
        根据问题、历史和知识构造Prompt。


        输入:

            question:
                当前问题

            history:
                对话历史

            chunks:
                检索结果


        输出:

            prompt:str
        """


        return self.prompt_builder.build(
            question=question,
            history=history,
            chunks=chunks
        )



    def generate(
        self,
        prompt: str
    ) -> str:
        """
        调用LLM生成回答。


        输入:

            prompt:str


        输出:

            answer:str
        """


        return self.llm_client.generate(
            prompt
        )



    def extract_references(
        self,
        chunks: list[Chunk]
    ) -> list[str]:
        """
        从Chunk中提取知识来源。


        输入:

            chunks


        输出:

            references列表


        示例:

        [
            "AVL.pdf page5",
            "tree.pdf page10"
        ]
        """


        references = []


        for chunk in chunks:

            source = chunk.metadata.get(
                "source",
                "unknown"
            )

            page = chunk.metadata.get(
                "page",
                -1
            )


            references.append(
                f"{source} page {page}"
            )


        return references
=======
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
>>>>>>> Stashed changes
