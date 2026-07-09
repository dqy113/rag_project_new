import streamlit as st
import os
import time
from datetime import datetime

from container import (
    chat_controller,
    knowledge_controller
)


# ==================================================
# 页面配置
# ==================================================

st.set_page_config(
    page_title="CS知识智能问答助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 初始化会话状态
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "new_doc_count" not in st.session_state:
    st.session_state.new_doc_count = 0

if "course_list" not in st.session_state:
    st.session_state.course_list = ["数据结构"]
if "tag_list" not in st.session_state:
    st.session_state.tag_list = ["教材", "课件", "习题"]

# ===== 新增：记录本次上传的文档 =====
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []  # 每个元素: {"filename": "xxx.pdf", "course": "数据结构", "tags": ["教材"]}


# ==================================================
# 标题区域
# ==================================================

st.markdown(
    """
    # 🤖 CS知识智能问答助手

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
                你的专属知识助手
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
    # 标签分类管理
    # ==================================================

    with st.expander("🏷️ 标签分类管理", expanded=False):

        st.markdown("### 📂 课程管理")
        st.caption(f"当前课程：{', '.join(st.session_state.course_list)}")

        col1, col2 = st.columns([3, 1])
        with col1:
            new_course = st.text_input("新课程", placeholder="输入课程名称", key="new_course_input", label_visibility="collapsed")
        with col2:
            if st.button("➕", key="add_course"):
                if new_course and new_course.strip():
                    if new_course.strip() not in st.session_state.course_list:
                        st.session_state.course_list.append(new_course.strip())
                        st.rerun()
                    else:
                        st.toast("课程已存在")

        if st.session_state.course_list:
            col3, col4 = st.columns([3, 1])
            with col3:
                del_course = st.selectbox(
                    "删除课程",
                    [""] + st.session_state.course_list,
                    key="del_course",
                    label_visibility="collapsed"
                )
            with col4:
                if st.button("🗑️", key="del_course_btn"):
                    if del_course:
                        st.session_state.course_list.remove(del_course)
                        st.rerun()

        st.divider()

        st.markdown("### 🏷️ 标签管理")
        st.caption(f"当前标签：{', '.join(st.session_state.tag_list)}")

        col5, col6 = st.columns([3, 1])
        with col5:
            new_tag = st.text_input("新标签", placeholder="输入标签名称", key="new_tag_input", label_visibility="collapsed")
        with col6:
            if st.button("➕", key="add_tag"):
                if new_tag and new_tag.strip():
                    if new_tag.strip() not in st.session_state.tag_list:
                        st.session_state.tag_list.append(new_tag.strip())
                        st.rerun()
                    else:
                        st.toast("标签已存在")

        if st.session_state.tag_list:
            col7, col8 = st.columns([3, 1])
            with col7:
                del_tag = st.selectbox(
                    "删除标签",
                    [""] + st.session_state.tag_list,
                    key="del_tag",
                    label_visibility="collapsed"
                )
            with col8:
                if st.button("🗑️", key="del_tag_btn"):
                    if del_tag:
                        st.session_state.tag_list.remove(del_tag)
                        st.rerun()

    # ==================================================
    # 上传文件（折叠）
    # ==================================================

    with st.expander("📤 上传学习资料", expanded=False):

        st.caption("支持 PDF / TXT / DOCX / PPTX")

        uploaded_files = st.file_uploader(
            "上传文件",
            type=["pdf", "txt", "docx", "pptx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if st.session_state.course_list:
            course = st.selectbox("课程名称", st.session_state.course_list)
        else:
            st.warning("请先在「标签分类管理」中添加课程")
            course = ""

        if st.session_state.tag_list:
            selected_tag = st.selectbox("标签", [""] + st.session_state.tag_list)
        else:
            st.warning("请先在「标签分类管理」中添加标签")
            selected_tag = ""

        if st.button("开始构建知识库"):

            if not uploaded_files:
                st.warning("请先选择文件")
            elif not course:
                st.warning("请先添加课程")
            else:
                total_files = len(uploaded_files)

                progress_bar = st.progress(0, text="准备上传...")
                status_text = st.empty()

                for idx, file in enumerate(uploaded_files):
                    progress = idx / total_files
                    progress_bar.progress(progress, text=f"正在处理: {file.name}")

                    try:
                        upload_dir = "data/uploads"
                        os.makedirs(upload_dir, exist_ok=True)
                        save_path = os.path.join(upload_dir, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())

                        tags = [selected_tag] if selected_tag else []

                        document = knowledge_controller.upload_document(
                            file_path=save_path,
                            course=course,
                            tags=tags
                        )

                        # ===== 记录本次上传的文档 =====
                        st.session_state.uploaded_docs.append({
                            "filename": file.name,
                            "course": course,
                            "tags": tags
                        })
                        st.session_state.new_doc_count += 1

                    except Exception as e:
                        st.error(f"❌ {file.name}失败:\n{str(e)}")

                progress_bar.progress(1.0, text="")
                status_text.success(f"✅ 全部 {total_files} 个文件上传完成！")
                time.sleep(1)

                st.rerun()

    # ==================================================
    # 知识库状态（只显示本次新增，按课程分组）
    # ==================================================

    with st.expander("📁 知识库状态", expanded=False):

        st.info(f"📄 本次新增文档：{st.session_state.new_doc_count} 份")

        if st.session_state.uploaded_docs:
            st.divider()
            st.markdown("### 📂 本次上传（按课程分类）")

            # 按课程分组
            course_docs = {}
            for doc in st.session_state.uploaded_docs:
                course_name = doc.get("course", "未分类")
                if course_name not in course_docs:
                    course_docs[course_name] = []
                course_docs[course_name].append(doc)

            for course_name, docs in course_docs.items():
                with st.expander(f"📘 {course_name}（{len(docs)} 份）", expanded=False):
                    for doc in docs:
                        tags_str = ", ".join(doc.get("tags", [])) if doc.get("tags") else "无标签"
                        st.write(f"📄 {doc['filename']}  🏷️ {tags_str}")
        else:
            st.caption("暂无本次新增文档")

    # ==================================================
    # 问答历史（含导出TXT）
    # ==================================================

    with st.expander("📋 问答历史", expanded=False):

        if len(st.session_state.messages) > 0:
            st.caption(f"共 {len(st.session_state.messages)} 条对话记录")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ 清空历史", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()

            with col2:
                # 导出为 TXT
                export_text = f"问答历史导出\n导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_text += "=" * 50 + "\n\n"
                for msg in st.session_state.messages:
                    role_label = "用户" if msg["role"] == "user" else "知识助手"
                    export_text += f"【{role_label}】\n{msg['content']}\n\n"

                if st.download_button(
                    label="📥 导出为 TXT",
                    data=export_text,
                    file_name=f"问答历史_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                ):
                    st.toast("✅ 导出成功！")
        else:
            st.caption("暂无历史记录")

    st.divider()
    st.caption("📌 系统状态：运行中 ✅")


# ==================================================
# 聊天区域
# ==================================================

# ===== 欢迎语/空状态 =====
if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div style="text-align:center;padding:60px 20px 40px 20px;">
            <div style="font-size:64px;margin-bottom:20px;">📚</div>
            <h2 style="color:#1e1b4b;">上传资料，开始学习</h2>
            <p style="color:#6b7280;font-size:16px;">
                上传您的课程教材、课件或习题集，<br>
                我可以帮您解答课程中的各种问题。
            </p>
            <p style="color:#9ca3af;font-size:14px;margin-top:20px;">
                💡 试试点击下方的快捷提问，或直接在输入框提问
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ===== 快捷提问（放在聊天区上方） =====
quick_questions = [
    "什么是栈？",
    "快速排序的时间复杂度是多少？",
    "数组和链表的区别是什么？",
    "什么是递归？"
]

cols = st.columns(len(quick_questions))
for i, q in enumerate(quick_questions):
    with cols[i]:
        if st.button(q, key=f"quick_{i}", use_container_width=True):
            st.session_state._quick_prompt = q
            st.rerun()

st.divider()

# ===== 历史消息 =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== 用户输入 =====
quick_prompt = st.session_state.get("_quick_prompt", "")
if quick_prompt:
    st.session_state._quick_prompt = ""

if prompt := st.chat_input("请问您想问什么？") or quick_prompt:
    if quick_prompt and not prompt:
        prompt = quick_prompt

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