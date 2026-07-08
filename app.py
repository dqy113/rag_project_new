import streamlit as st
import os

from container import (
    chat_controller,
    knowledge_controller
)


# ==================================================
# 页面配置
# ==================================================

st.set_page_config(
    page_title="智能问答助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 标题区域
# ==================================================

st.markdown(
    """
    # 📚 CS知识智能问答系统

    > 基于 RAG 技术，面向课程教材的智能问答助手
    """
)

st.divider()


# ==================================================
# 侧边栏
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:12px 0 20px 0;">
            <div style="font-size:48px;">📚</div>
            <div style="font-weight:600;font-size:18px;">
                智能问答
            </div>
            <div style="font-size:12px;color:#6b7280;">
                数据结构 · RAG
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ==================================================
    # 上传文件（折叠）
    # ==================================================

    with st.expander("📤 上传学习资料", expanded=False):

        st.markdown("### 📤 上传学习资料")
        st.caption("支持 PDF / TXT / DOCX / PPTX")

        uploaded_files = st.file_uploader(
            "上传文件",
            type=["pdf", "txt", "docx", "pptx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        course = st.text_input("课程名称", value="数据结构")
        tags_input = st.text_input("标签(逗号分隔)", value="教材")

        if st.button("开始构建知识库"):

            if not uploaded_files:
                st.warning("请先选择文件")
            else:
                for file in uploaded_files:
                    with st.spinner(f"正在处理 {file.name}..."):
                        try:
                            # 保存上传文件
                            upload_dir = "data/uploads"
                            os.makedirs(upload_dir, exist_ok=True)
                            save_path = os.path.join(upload_dir, file.name)
                            with open(save_path, "wb") as f:
                                f.write(file.getbuffer())

                            # 标签处理
                            tags = [
                                tag.strip()
                                for tag in tags_input.split(",")
                                if tag.strip()
                            ]

                            # 调用Controller
                            document = knowledge_controller.upload_document(
                                file_path=save_path,
                                course=course,
                                tags=tags
                            )

                            st.success(f"✅ {document.filename} 构建完成")

                        except Exception as e:
                            st.error(f"❌ {file.name}失败:\n{str(e)}")

                st.rerun()

    # ==================================================
    # 知识库状态（折叠）
    # ==================================================

    with st.expander("📁 知识库状态", expanded=False):

        try:
            documents = knowledge_controller.get_documents()
            st.info(f"📄 已加载文档：{len(documents)} 份")
        except Exception as e:
            documents = []
            st.warning("知识库初始化失败")

    st.divider()
    st.caption("📌 系统状态：运行中 ✅")


# ==================================================
# 聊天区域
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("请问您想问什么？"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.spinner("AI 正在检索知识库并思考中..."):
        try:
            response = chat_controller.ask(prompt)
            answer = response.answer
        except Exception as e:
            answer = f"【系统错误】{str(e)}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==================================================
# Footer
# ==================================================

if st.session_state.messages:
    st.divider()
    st.caption("🔍 上传资料，获得更精准的回答")