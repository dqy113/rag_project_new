# backend/models/response.py

from dataclasses import dataclass, field
from typing import List


@dataclass
class AnswerResponse:
    """
    RAG系统最终返回结果。
    """

    # AI生成答案
    answer: str


    # 引用来源
    references: List[str] = field(
        default_factory=list
    )


    # 生成耗时
    latency: float = 0.0


    # 是否成功
    success: bool = True


    # 错误信息
    error_message: str = ""
