# backend/service/conversation_service.py

import json
import os

from typing import List

from backend.models.conversation import Conversation


class ConversationService:
    """
    对话管理服务。

    负责:
    1. 保存用户和AI的历史消息
    2. 提供多轮对话上下文
    3. 持久化聊天记录

    不负责:
    - RAG检索
    - Prompt生成
    - LLM调用
    """


    def __init__(
        self,
        history_file: str = "data/history/chat_history.json",
        max_history: int = 5
    ):
        """
        初始化ConversationService。


        参数:

            history_file:
                历史记录保存路径


            max_history:
                保留最近多少轮聊天
        """

        self.history_file = history_file

        self.max_history = max_history


        # 当前会话缓存
        self.messages: List[Conversation] = []


        # 启动时加载历史
        self.load_history()



    def add_message(
        self,
        question: str,
        answer: str,
        references: list[str] = None
    ):
        """
        添加一轮聊天记录。


        输入:

            question:
                用户问题


            answer:
                AI回答


            references:
                使用到的知识来源


        输出:

            None
        """


        conversation = Conversation(

            question=question,

            answer=answer,

            references=(
                references
                if references
                else []
            )

        )


        self.messages.append(
            conversation
        )


        # 限制历史长度
        if len(self.messages) > self.max_history:

            self.messages = (
                self.messages[-self.max_history:]
            )


        # 保存
        self.save_history()



    def get_history(
        self
    ) -> List[Conversation]:
        """
        获取完整历史记录。


        输出:

            List[Conversation]
        """

        return self.messages



    def get_context(
        self
    ) -> str:
        """
        获取用于Prompt的历史上下文。


        输出:

            history:str


        示例:

            用户:
            什么是AVL？

            助手:
            AVL是一种...
        """


        context = []


        for message in self.messages:


            context.append(
                f"""
用户:
{message.question}

助手:
{message.answer}
"""
            )


        return "\n".join(context)



    def clear(
        self
    ):
        """
        清空当前聊天记录。
        """


        self.messages.clear()


        self.save_history()



    def save_history(
        self
    ):
        """
        将聊天记录保存到JSON文件。
        """


        directory = os.path.dirname(
            self.history_file
        )


        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )


        data = []


        for item in self.messages:

            data.append(
                {
                    "question":
                    item.question,

                    "answer":
                    item.answer,

                    "references":
                    item.references,

                    "timestamp":
                    item.timestamp
                }
            )


        with open(
            self.history_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )



    def load_history(
        self
    ):
        """
        从JSON恢复历史记录。
        """


        if not os.path.exists(
            self.history_file
        ):
            return


        with open(
            self.history_file,
            "r",
            encoding="utf-8"
        ) as f:


            data = json.load(f)



        for item in data:


            conversation = Conversation(

                question=item["question"],

                answer=item["answer"],

                references=item.get(
                    "references",
                    []
                )

            )


            self.messages.append(
                conversation
            )
