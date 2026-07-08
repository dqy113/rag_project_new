# backend/llm/llm_client.py

import os
import time
from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = (
    Path(__file__)
    .resolve()
    .parents[2]
    /
    ".env"
)

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True
)


from zhipuai import ZhipuAI
from backend.utils.logger import logger




class LLMClient:
    """
    大语言模型调用客户端。

    负责:
    1. 管理LLM API连接
    2. 构造请求
    3. 调用模型
    4. 返回生成结果


    当前实现:
        智谱 GLM

    后续可扩展:
        GPT
        DeepSeek
        Claude
    """


    def __init__(
        self,
        model_name: str = "glm-4"
    ):

        self.model_name = model_name


        api_key = os.getenv(
            "ZHIPUAI_API_KEY"
        )


        if not api_key:

            logger.error(
                "未找到 ZHIPUAI_API_KEY"
            )

            raise ValueError(
                "Missing API Key"
            )


        self.client = ZhipuAI(
            api_key=api_key
        )



    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        trace_id: str = ""
    ) -> str:
        """
        调用大模型生成回答。


        输入:

            prompt:
                PromptBuilder生成的完整Prompt


            system_prompt:
                系统角色设定


            temperature:
                随机性参数


            trace_id:
                请求追踪ID


        输出:

            answer:str
        """


        start_time = time.time()



        if system_prompt is None:

            system_prompt = (
                "你是一个基于知识库回答问题的AI助手。"
            )



        logger.info(
            f"[{trace_id}] "
            f"开始调用LLM: {self.model_name}"
        )


        logger.debug(
            f"[{trace_id}] Prompt:\n{prompt}"
        )



        try:


            response = (
                self.client.chat.completions.create(

                    model=self.model_name,

                    messages=[
                        {
                            "role":
                            "system",

                            "content":
                            system_prompt
                        },

                        {
                            "role":
                            "user",

                            "content":
                            prompt
                        }
                    ],

                    temperature=temperature
                )
            )



            answer = (
                response
                .choices[0]
                .message
                .content
            )



            latency = (
                time.time()
                -
                start_time
            )


            # token统计
            if hasattr(
                response,
                "usage"
            ):

                usage = response.usage


                logger.info(
                    f"[{trace_id}] "
                    f"LLM完成 "
                    f""
                    f"Prompt Tokens:"
                    f"{usage.prompt_tokens}, "
                    f"Completion Tokens:"
                    f"{usage.completion_tokens}, "
                    f"Total:"
                    f"{usage.total_tokens}"
                )


            logger.info(
                f"[{trace_id}] "
                f"LLM耗时:{latency:.2f}s"
            )


            return answer



        except Exception as e:


            logger.exception(
                f"[{trace_id}] "
                f"LLM调用失败:{str(e)}"
            )


            raise e



    def health_check(self) -> bool:
        """
        检查LLM服务是否可用。


        输出:

            True / False
        """


        try:

            return self.client is not None


        except Exception:

            return False