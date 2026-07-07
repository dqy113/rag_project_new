# backend/retrieval/prompt_builder.py

from backend.models.chunk import Chunk


class PromptBuilder:
    """
    Prompt构建模块。

    负责将:
    - System角色
    - 对话历史
    - 检索知识
    - 用户问题

    组合成发送给LLM的完整Prompt。
    """

    def __init__(
        self,
        system_prompt: str = None
    ):
        """
        初始化PromptBuilder。


        输入:

            system_prompt:
                AI角色设定

        """

        self.system_prompt = (
            system_prompt
            if system_prompt
            else
            """
            你是一名专业的数据结构课程助教。
            请根据提供的知识库内容回答问题。
            如果知识库中没有相关信息，
            请明确说明无法确定。
            """
        )


    def build(
        self,
        question: str,
        history: str,
        chunks: list[Chunk]
    ) -> str:
        """
        构建最终Prompt。


        输入:

            question:
                当前用户问题


            history:
                历史聊天上下文


            chunks:
                Retriever返回的知识片段


        输出:

            prompt:str
        """


        context = self.build_context(
            chunks
        )


        history_text = (
            history
            if history
            else
            "暂无历史对话"
        )


        prompt = f"""
{self.system_prompt}


===== 对话历史 =====

{history_text}


===== 知识库内容 =====

{context}


===== 用户问题 =====

{question}


请根据以上知识回答用户问题。
回答要求:
1. 优先使用知识库内容。
2. 不要编造不存在的信息。
3. 如果引用知识，请说明来源。


答案:
"""


        return prompt



    def build_context(
        self,
        chunks: list[Chunk]
    ) -> str:
        """
        将Chunk转换为知识上下文。


        输入:

            list[Chunk]


        输出:

            context:str
        """


        contexts = []


        for index, chunk in enumerate(chunks):

            source = chunk.metadata.get(
                "source",
                "unknown"
            )

            page = chunk.metadata.get(
                "page",
                ""
            )


            text = f"""
知识片段{index + 1}

来源:
{source}

页码:
{page}

内容:
{chunk.content}

"""


            contexts.append(text)


        return "\n".join(
            contexts
        )



    def build_history(
        self,
        history: list
    ) -> str:
        """
        格式化历史聊天。


        输入:

            Conversation列表


        输出:

            history字符串
        """


        result = []


        for item in history:

            result.append(
                f"""
用户:
{item.question}

助手:
{item.answer}
"""
            )


        return "\n".join(result)



    def update_system_prompt(
        self,
        prompt:str
    ):
        """
        更新角色Prompt。


        输入:

            新Prompt


        输出:

            None
        """

        self.system_prompt = prompt