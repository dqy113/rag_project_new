import os
from dotenv import load_dotenv


print("当前路径:")
print(os.getcwd())


load_dotenv()


print("API KEY:")
print(os.getenv("ZHIPUAI_API_KEY"))