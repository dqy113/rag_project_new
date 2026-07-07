# backend/models/document.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class Document:
    """
    表示系统中的一个知识文档。

    一个Document对应用户上传的一个文件，
    例如一个PDF教材、一份课程讲义。
    """

    id: str
    filename: str

    # 文档原始文本内容
    content: str

    # 文档额外信息
    # 例如:
    # {
    #   "page": 5,
    #   "author": "xxx"
    # }
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 上传时间
    upload_time: str = field(
        default_factory=lambda:
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # 文件类型
    file_type: str = ""
