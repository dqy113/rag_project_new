# backend/llm/llm_client.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.utils.logger import logger

load_dotenv()


class ZhipuLLMClient:
    def __init__(self):
        self.api_key = os.getenv("ZHIPU_API_KEY")
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/"
        if not self.api_key:
            logger.error("【大模型层】本地系统环境变量缺失 ZHIPU_API_KEY！")

    def get_llm_response(self, prompt: str, trace_id: str = "SYSTEM") -> str:
        """向智谱大模型推送最终组装的 Prompt"""
        if not self.api_key:
            return "【错误】本地未检测到 API Key，请检查根目录的 .env 文件！"

        logger.info(f"[{trace_id}] 【大模型层】正在请求智谱大模型 (glm-4-flash)...")
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            logger.info(f"[{trace_id}] 【大模型层】智谱大模型返回响应成功。")
            return response.choices[0].message.content
        except Exception as e:
            logger.exception(f"[{trace_id}] 【大模型层】大模型 API 在线调用中断")
            return f"【AI调用失败】原因: {str(e)}"