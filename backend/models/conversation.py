# backend/models/conversation.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Conversation:
    """
    表示一次完整聊天记录。
    """

    # 用户问题
    question: str


    # AI回答
    answer: str


    # 使用到的知识引用
    #
    # 例如:
    # [
    #   "AVL.pdf page10"
    # ]
    references: List[str] = field(
        default_factory=list
    )


    # 时间
    timestamp: str = field(
        default_factory=lambda:
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
