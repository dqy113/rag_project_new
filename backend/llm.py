# backend/llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 自动寻找并读取根目录下的 .env 文件
load_dotenv()

def get_llm_response(prompt: str) -> str:
    """调用智谱 AI 的函数"""
    # 2. 从系统环境里抓取你的钥匙
    api_key = os.getenv("ZHIPU_API_KEY")
    
    # 智谱标准的官方调用网址
    base_url = "https://open.bigmodel.cn/api/paas/v4/"
    
    if not api_key:
        return "【错误】本地未检测到 API Key，请检查根目录的 .env 文件！"
        
    try:
        # 3. 初始化客户端并发送请求
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model="glm-4-flash",  # 智谱提供给新手的免费轻量模型
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"【AI调用失败】原因: {str(e)}"

# === 以下是测试代码 ===
# 只要在这个文件里直接右键运行，就能看到大模型有没有回答你

#if __name__ == "__main__":
    print("正在连接智谱大模型...")
    test_reply = get_llm_response("你好，请问什么是冒泡排序？用一句话回答。")
    print("\n--- 大模型回复如下 ---")
    print(test_reply)
