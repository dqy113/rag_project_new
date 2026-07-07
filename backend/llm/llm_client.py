# backend/llm/llm_client.py
import os
from zhipuai import ZhipuAI
from backend.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()


class ZhipuLLMClient:
    def __init__(self):
        # 从环境变量加载智谱 API Key
        api_key = os.getenv("ZHIPUAI_API_KEY")
        if not api_key:
            logger.error("未在环境变量中找到 ZHIPUAI_API_KEY，请检查 .env 文件！")
        self.client = ZhipuAI(api_key=api_key)

    def chat_completion(self, prompt: str, system_prompt: str = "你是一个智能助手", model: str = "glm-4",
                        temperature: float = 0.7, trace_id: str = "") -> str:
        """
        请求智谱大模型，并精准记录工程日志
        """
        logger.info(f"[{trace_id}] 开始请求智谱大模型 [{model}]...")
        logger.debug(f"[{trace_id}] Prompt 详情 -> System: {system_prompt} | User: {prompt}")

        try:
            # 组装智谱标准输入格式
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            # 发起请求
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )

            # 解析智谱返回的元数据
            content = response.choices[0].message.content
            usage = response.usage

            # 核心：将 Token 消耗和响应状态打入工程日志文件
            logger.info(
                f"[{trace_id}] 智谱大模型响应成功. "
                f"Prompt Tokens: {usage.prompt_tokens} | "
                f"Completion Tokens: {usage.completion_tokens} | "
                f"Total Tokens: {usage.total_tokens}"
            )

            return content

        except Exception as e:
            # 发生异常时，自动捕获代码堆栈，非常方便排查网络或认证错误
            logger.exception(f"[{trace_id}] 请求智谱大模型发生异常: {str(e)}")
            raise e