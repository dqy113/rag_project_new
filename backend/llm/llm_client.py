# backend/llm/llm_client.py

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from zhipuai import ZhipuAI

from backend.utils.logger import logger



class LLMClient:
    """
    大语言模型客户端

    负责:
    1. 加载API Key
    2. 初始化LLM连接
    3. 发送Prompt
    4. 返回生成结果
    """

    def __init__(
        self,
        model_name: str = "glm-4"
    ):

        self.model_name = model_name


        # ==========================
        # 加载项目根目录.env
        # ==========================

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )


        env_path = (
            project_root
            /
            ".env"
        )


        load_dotenv(
            env_path,
            override=True
        )


        # ==========================
        # 获取API Key
        # ==========================

        api_key = os.environ.get(
            "ZHIPUAI_API_KEY"
        )


        if not api_key:

            logger.error(
                f"未找到API Key, env路径:{env_path}"
            )

            raise ValueError(
                "Missing API Key"
            )


        logger.info(
            "ZhipuAI API Key加载成功"
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
        调用大模型生成回答

        输入:
            prompt:
                用户Prompt

            system_prompt:
                系统角色

            temperature:
                随机程度


        输出:
            str
        """


        start_time = time.time()


        if system_prompt is None:

            system_prompt = (
                "你是一个基于知识库回答问题的AI助手，"
                "请根据提供的信息回答，不要编造。"
            )


        logger.info(
            f"[{trace_id}] "
            f"开始调用LLM {self.model_name}"
        )


        try:


            response = (
                self.client
                .chat
                .completions
                .create(

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
                    f"Tokens:"
                    f"{usage.total_tokens}"
                )


            logger.info(
                f"[{trace_id}] "
                f"LLM完成 "
                f"耗时:{latency:.2f}s"
            )


            return answer



        except Exception as e:


            logger.exception(
                f"[{trace_id}] "
                f"LLM调用失败:{e}"
            )


            raise e



    def health_check(self) -> bool:
        """
        检查客户端是否初始化成功
        """

        return self.client is not None