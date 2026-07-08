# backend/controller/chat_controller.py

from backend.service.rag_service import RAGService
from backend.service.conversation_service import ConversationService
from backend.models.response import AnswerResponse


class ChatController:
    """
    聊天请求控制器。

    负责接收用户问题，
    调用RAGService完成问答，
    返回AnswerResponse。
    """

    def __init__(
        self,
        rag_service: RAGService,
        conversation_service: ConversationService
    ):
        """
        初始化Controller。

        输入:
            rag_service:
                RAG核心服务

            conversation_service:
                对话历史管理服务
        """

        self.rag_service = rag_service

        self.conversation_service = conversation_service



    def ask(
        self,
        question: str
    ) -> AnswerResponse:
        """
        用户提问入口。

        流程:
        1. 获取历史上下文
        2. 调用RAG生成答案
        3. 保存本轮对话
        4. 返回结果


        输入:
            question:
                用户问题


        输出:
            AnswerResponse
        """


        # 1. 获取历史对话
        history = (
            self.conversation_service
            .get_context()
        )


        # 2. 调用RAG核心流程
        response = (
            self.rag_service
            .answer(
                question,
                history
            )
        )


        # 3. 保存本轮聊天
        self.conversation_service.add_message(
            question,
            response.answer,
            response.references
        )


        # 4. 返回
        return response



    def get_history(self):
        """
        获取历史聊天记录。

        输入:
            无

        输出:
            List[Conversation]
        """

        return (
            self.conversation_service
            .get_history()
        )



    def clear_history(self):
        """
        清空聊天记录。

        输入:
            无

        输出:
            bool
        """

        return (
            self.conversation_service
            .clear()
        )