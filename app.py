import streamlit as st
import os
from backend.rag import ask

# ===== 页面配置 =====
st.set_page_config(
    page_title="数据结构智能问答系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 初始化登录状态 =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# ===== 登录页面（未登录时显示） =====
# ============================================================
if not st.session_state.logged_in:

    st.markdown("""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <div style="font-size: 64px;">📚</div>
        <h1>数据结构智能问答系统</h1>
        <p style="color: #6b7280; font-size: 16px;">基于 RAG 校本专属知识库</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👤 登录")

        # 身份选择
        role = st.radio(
            "选择身份",
            ["🎓 学生", "👨‍🏫 教师"],
            horizontal=True
        )

        # 学号/工号
        username = st.text_input(
            "学号 / 工号",
            placeholder="请输入学号或工号"
        )

        # 密码
        password = st.text_input(
            "密码",
            type="password",
            placeholder="请输入密码"
        )

        # 登录按钮
        if st.button("🔑 登录", type="primary", use_container_width=True):

            if not username or not password:
                st.warning("⚠️ 请完整填写账号和密码")
            else:
                # 模拟验证：硬编码测试账号
                if username == "admin" and password == "123456":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "teacher"
                    st.session_state.username = username
                    st.rerun()
                elif username == "student" and password == "123456":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ 账号或密码错误，请重新输入")

        st.caption("💡 测试账号：admin / 123456（教师） | student / 123456（学生）")

    st.stop()  # 登录后不再执行下面代码


# ============================================================
# ===== 登录后的主界面 =====
# ============================================================

# 顶部提示
if st.session_state.user_role == "teacher":
    st.success(f"👨‍🏫 教师管理员：{st.session_state.username}，欢迎回来！")
else:
    st.info(f"🎓 学生：{st.session_state.username}，欢迎回来！")

st.markdown("""
# 📚 数据结构知识智能问答系统
> 基于 RAG 校本专属知识库，精准贴合教学大纲与课堂内容
""")

st.divider()

# ===== 侧边栏 =====
with st.sidebar:
    # Logo 区域
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 20px 0;">
        <div style="font-size: 48px;">📚</div>
        <div style="font-weight: 600; font-size: 18px; color: #1e1b4b;">智能问答</div>
        <div style="font-size: 12px; color: #6b7280;">数据结构 · RAG</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ===== 当前用户信息 =====
    st.markdown("### 👤 当前用户")
    if st.session_state.user_role == "teacher":
        st.info("👨‍🏫 教师管理员")
    else:
        st.info("🎓 学生")
    st.caption(f"账号：{st.session_state.username}")

    # 退出登录
    if st.button("🚪 退出登录"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = ""
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # ===== 知识库状态 =====
    st.markdown("### 📁 知识库状态")
    data_dir = "data"
    if os.path.exists(data_dir):
        doc_files = [f for f in os.listdir(data_dir) if f.endswith(('.pdf', '.txt', '.docx', '.pptx'))]
        doc_count = len(doc_files)
        st.info(f"📄 已加载文档：{doc_count} 份")
    else:
        st.info("📄 知识库：暂无文档")

    st.divider()

    # ============================================================
    # ===== 学生功能 =====
    # ============================================================
    st.markdown("### 📋 我的历史记录")
    if len(st.session_state.messages) > 0:
        st.caption(f"共 {len(st.session_state.messages)} 条对话记录")
        if st.button("🗑️ 清空历史记录"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.caption("暂无历史记录")

    st.divider()

    # ============================================================
    # ===== 教师功能（仅教师可见） =====
    # ============================================================
    if st.session_state.user_role == "teacher":
        st.markdown("### 🔧 知识库管理")
        st.caption("管理员专属功能")

        # 批量上传
        st.markdown("#### 📤 批量上传文档")
        st.caption("支持格式：PDF、Word、TXT、PPTX")

        uploaded_files = st.file_uploader(
            "点击选择文件或拖拽至此",
            type=["pdf", "txt", "docx", "pptx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        SAVE_DIR = "data"
        os.makedirs(SAVE_DIR, exist_ok=True)

        if uploaded_files:
            for file in uploaded_files:
                with st.spinner(f"正在处理 {file.name}..."):
                    save_path = os.path.join(SAVE_DIR, file.name)
                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())
                    st.success(f"✅ {file.name} 上传成功！")
            st.rerun()

        st.divider()

        # 知识库分类
        st.markdown("#### 📂 知识库分类")
        categories = ["线性表", "栈与队列", "串", "树与二叉树", "图", "排序", "查找"]
        for cat in categories:
            st.checkbox(cat, value=True)

        st.divider()

        # 知识内容审核
        st.markdown("#### ✏️ 知识内容审核")
        st.caption("待审核知识条目：3 条")
        if st.button("📋 查看待审核条目"):
            st.info("1. 栈与队列 - 入栈出栈操作（待确认）\n2. 二叉树遍历 - 先序遍历（待修改）\n3. 快速排序 - 时间复杂度（待更新）")

    else:
        # 学生侧边栏底部提示
        st.caption("💡 教师可切换至管理员模式管理知识库")

# ============================================================
# ===== 聊天区域 =====
# ============================================================

# 显示历史聊天内容
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "source" in msg and msg["source"]:
            st.caption(f"📖 来源：{msg['source']}")

# 接受用户输入
if prompt := st.chat_input("请问您想问什么？"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AI 正在检索校本知识库并思考中..."):
        try:
            response = ask(prompt)
            if isinstance(response, dict):
                answer = response.get("answer", str(response))
                source = response.get("source", "")
            else:
                answer = str(response)
                source = ""
        except Exception as e:
            answer = f"【系统错误】后端调用失败，原因: {str(e)}"
            source = ""

    with st.chat_message("assistant"):
        st.markdown(answer)
        if source:
            st.caption(f"📖 来源：{source}")

        st.divider()
        st.caption("💡 基于 RAG 的数据结构知识问答系统 | 知识来源：本校课程讲义与教材")

    st.session_state.messages.append({"role": "assistant", "content": answer, "source": source})