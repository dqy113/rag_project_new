from backend.llm import get_llm_response
from backend.vector_store import search_relevant_docs  # 🌟 导入检索函数

# 兼容处理：尝试导入主入口的检索函数，失败则降级
try:
    from main import search_knowledge
except Exception:
    search_knowledge = None


def ask(user_question: str) -> str:
    """
    最终留给前端 app.py 调用的核心接口
    """
    # 1. 真正的 RAG 第一步：去知识库里找相关的参考资料
    if search_knowledge:
        docs = search_knowledge(user_question, top_k=3)
        # 兼容处理：如果返回的是对象则取 page_content，否则转为字符串
        context = "\n\n".join([getattr(doc, "page_content", str(doc)) for doc in docs])
    else:
        # 如果 main 里的 search_knowledge 不可用，用 vector_store 的兜底
        context = search_relevant_docs(user_question, k=3)

    # 2. 真正的 RAG 第二步：把检索到的知识与你的【严格答题规则】合并，作为背景补充给大模型
    rag_prompt = f"""你是一个专业的数据结构智能助教。请严格根据以下给出的【已知知识库信息】来回答用户的【问题】。

【回答规则】：
1. 严格依据下面的知识库内容回答，禁止编造不存在的信息；
2. 涉及算法时间/空间复杂度等数学表达式时，必须使用标准Markdown公式格式：
   - 平方写成 $O(n^2)$，绝对不能简写为n2；
   - 对数写成 $O(n\\log_2 n)$，不能简写log2n；
   - 所有复杂度公式前后用 $ 符号包裹；
3. 术语不能混淆：严格区分「最好情况」「平均情况」「最坏情况」，不要写错文字；
4. 如果已知信息里无法回答该问题，请礼貌地回答你不知道，不要瞎编。

【已知知识库信息】：
{context}

【用户的实际问题】：
{user_question}
"""

    # 3. 真正的 RAG 第三步：把拼好的大 Prompt 扔给大模型
    final_answer = get_llm_response(rag_prompt)
    return final_answer