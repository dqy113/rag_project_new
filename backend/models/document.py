from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Document:
    """
    知识库文档模型

    表示用户上传的一份课程资料。
    """

    # 唯一编号
    document_id: str


    # 文件名称
    filename: str


    # 文件路径
    filepath: str


    # 文件类型
    file_type: str

    # 文档原始文本内容
    content: str = ""


    # 原始metadata
    metadata: dict = field(
        default_factory=dict
    )


    # 所属课程
    # 例如：
    # 数据结构
    # CSAPP
    course: str = "default"


    # 章节信息
    # 例如：
    # ["树", "AVL"]
    chapters: List[str] = field(
        default_factory=list
    )


    # 标签
    # 例如：
    # ["排序", "复杂度"]
    tags: List[str] = field(
        default_factory=list
    )


    # 上传时间
    upload_time: str = field(
        default_factory=lambda:
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # 状态
    # uploading
    # processing
    # ready
    # failed
    status: str = "ready"


    # 生成chunk数量
    chunk_count: int = 0