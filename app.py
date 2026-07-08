import streamlit as st
import os

# ===== 从 container 导入已初始化好的控制器 =====
from container import chat_controller

# ============================================================
# ===== 页面配置 =====
# ============================================================
st.set_page_config(
    page_title="个人课程知识增强学习助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ===== 初始化会话状态 =====
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "courses" not in st.session_state:
    st.session_state.courses = ["CSAPP"]
if "selected_courses" not in st.session_state:
    st.session_state.selected_courses = ["CSAPP"]
if "new_course" not in st.session_state:
    st.session_state.new_course = ""

# ============================================================
# ===== 侧边栏各板块渲染函数 =====
# ============================================================

def render_logo():
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 20px 0;">
        <div style="font-size: 48px;">📚</div>
        <div style="font-weight: 600; font-size: 18px; color: #1e1b4b;">学习助手</div>
        <div style="font-size: 12px; color: #6b7280;">个人知识库 · RAG</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()


def render_course_management():
    """课程管理：多选下拉框，勾选当前学习的课程"""
    st.markdown("### 📖 课程管理")

    if st.session_state.selected_courses:
        st.caption(f"当前选中：{', '.join(st.session_state.selected_courses)}")
    else:
        st.caption("未选择任何课程，将检索全部资料")

    # 用 form 包裹，防止滚动弹跳
    with st.form(key="course_form", clear_on_submit=False):
        if st.session_state.courses:
            selected = st.multiselect(
                "选择课程",
                options=st.session_state.courses,
                default=st.session_state.selected_courses,
                key="course_multiselect",
                label_visibility="collapsed",
                placeholder="选择正在学习的课程..."
            )
        else:
            st.caption("暂无课程，请添加")
            selected = []

        if st.form_submit_button("确认选择", use_container_width=False):
            if selected != st.session_state.selected_courses:
                st.session_state.selected_courses = selected
                st.rerun()

    # 添加课程（一行内：输入框 + 小➕按钮）
    col_add1, col_add2 = st.columns([5, 1])
    with col_add1:
        new_course = st.text_input(
            "课程名",
            placeholder="添加新课程...",
            key="new_course_input",
            label_visibility="collapsed"
        )
    with col_add2:
        if st.button("➕", key="add_course_btn", use_container_width=True):
            if new_course and new_course.strip():
                course_name = new_course.strip()
                if course_name not in st.session_state.courses:
                    st.session_state.courses.append(course_name)
                    st.session_state.selected_courses.append(course_name)
                    st.rerun()
                else:
                    st.toast(f"⚠️ '{course_name}' 已存在")

    # 删除课程（一行内：下拉框 + 小🗑️按钮）
    col_del1, col_del2 = st.columns([5, 1])
    with col_del1:
        if st.session_state.courses:
            course_to_delete = st.selectbox(
                "删除课程",
                options=st.session_state.courses,
                key="course_delete_select",
                label_visibility="collapsed",
                placeholder="选择要删除的课程..."
            )
        else:
            st.caption("无课程可删除")
            course_to_delete = None
    with col_del2:
        if st.button("🗑️", key="delete_course_btn", use_container_width=True):
            if course_to_delete and course_to_delete in st.session_state.courses:
                st.session_state.courses.remove(course_to_delete)
                if course_to_delete in st.session_state.selected_courses:
                    st.session_state.selected_courses.remove(course_to_delete)
                st.rerun()

    st.divider()


def render_upload_section():
    """上传资料（带课程标签）"""
    st.markdown("### 📤 上传课程资料")

    if not st.session_state.courses:
        st.warning("⚠️ 请先在「课程管理」中添加课程")
        st.divider()
        return

    selected_course = st.selectbox(
        "选择所属课程",
        options=st.session_state.courses,
        key="upload_course_select",
        placeholder="请选择资料对应的课程..."
    )

    st.caption("支持格式：PDF、Word、TXT、PPTX")

    uploaded_files = st.file_uploader(
        "点击选择文件或拖拽至此",
        type=["pdf", "txt", "docx", "pptx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    SAVE_DIR = "data"
    os.makedirs(SAVE_DIR, exist_ok=True)

    if uploaded_files and selected_course:
        for file in uploaded_files:
            with st.spinner(f"正在处理 {file.name}..."):
                save_path = os.path.join(SAVE_DIR, f"[{selected_course}]_{file.name}")
                with open(save_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"✅ {file.name} → {selected_course}")
        st.rerun()

    st.divider()


def render_doc_library():
    """我的资料库（按课程筛选）"""
    st.markdown("### 📚 我的资料库")

    data_dir = "data"
    if not os.path.exists(data_dir):
        st.caption("暂无资料")
        st.divider()
        return

    all_files = [f for f in os.listdir(data_dir) if f.endswith(('.pdf', '.txt', '.docx', '.pptx'))]

    if not all_files:
        st.caption("暂无资料")
        st.divider()
        return

    # 从文件名中提取课程名
    available_courses = []
    for f in all_files:
        if f.startswith("[") and "]" in f:
            course = f.split("]")[0].replace("[", "")
            if course not in available_courses:
                available_courses.append(course)

    if not available_courses:
        available_courses = ["未分类"]

    filter_course = st.selectbox(
        "筛选课程",
        options=["全部"] + available_courses,
        key="doc_filter_course"
    )

    if filter_course == "全部":
        filtered_files = all_files
    else:
        filtered_files = [f for f in all_files if f.startswith(f"[{filter_course}]")]

    if not filtered_files:
        st.caption("该课程暂无资料")
        st.divider()
        return

    st.caption(f"共 {len(filtered_files)} 份资料")

    for doc in sorted(filtered_files):
        col1, col2 = st.columns([5, 1])
        with col1:
            display_name = doc.split("]_", 1)[-1] if "]_" in doc else doc
            st.write(f"📄 {display_name}")
        with col2:
            if st.button("🗑️", key=f"del_{doc}"):
                os.remove(os.path.join(data_dir, doc))
                st.rerun()

    st.divider()


def render_history():
    st.markdown("### 📋 问答历史")
    if len(st.session_state.messages) > 0:
        st.caption(f"共 {len(st.session_state.messages)} 条对话记录")
        if st.button("🗑️ 清空历史记录"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.caption("暂无历史记录")
    st.divider()


def render_footer():
    st.caption("💡 系统状态：运行中 ✅")


# ============================================================
# ===== 主界面标题 =====
# ============================================================
st.markdown("""
# 📚 个人课程知识增强学习助手
> 基于 RAG 个人专属知识库，精准溯源，拒绝幻觉
""")
st.divider()

# ============================================================
# ===== 侧边栏 =====
# ============================================================
with st.sidebar:
    render_logo()
    render_course_management()
    render_upload_section()
    render_doc_library()
    render_history()
    render_footer()


# ============================================================
# ===== 聊天区域 =====
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "source" in msg and msg["source"]:
            st.caption(f"📖 来源：{msg['source']}")

if prompt := st.chat_input("请输入您的课程问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("正在检索知识库并生成回答..."):
        try:
            # ===== 调用 chat_controller，传入当前选中的课程列表 =====
            response = chat_controller.ask(
                question=prompt,
                course_filter=st.session_state.selected_courses
            )
            answer = response.answer
            source = ", ".join(response.references) if response.references else ""
        except Exception as e:
            answer = f"【系统错误】调用失败，原因: {str(e)}"
            source = ""

    with st.chat_message("assistant"):
        st.markdown(answer)
        if source:
            st.caption(f"📖 来源：{source}")
        st.divider()
        st.caption(f"💡 基于个人知识库生成 | 课程：{', '.join(st.session_state.selected_courses) if st.session_state.selected_courses else '全部'}")

    st.session_state.messages.append({"role": "assistant", "content": answer, "source": source})