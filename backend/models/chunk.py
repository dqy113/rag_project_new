# backend/models/chunk.py

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Chunk:
    """
    RAG系统中的最小知识检索单位。

    一个Chunk会被Embedding，
    然后存入向量数据库。
    """

    id: str

    # 属于哪个Document
    document_id: str

    # Chunk文本内容
    content: str


    # 元数据
    #
    # 例如:
    # {
    #    "source":"AVL.pdf",
    #    "page":10
    # }
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    # Embedding后的向量
    #
    # 例如:
    # [
    #    0.123,
    #    0.456
    # ]
    embedding: List[float] = field(
        default_factory=list
    )
