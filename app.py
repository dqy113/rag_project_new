import streamlit as st
import os
from backend.rag import ask

# ===== 页面配置 =====
st.set_page_config(
    page_title="数据结构智能问答助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 标题区域 =====
st.markdown("""
# 📚 数据结构知识智能问答系统
> 基于 RAG 技术，回答数据结构相关问题
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
    
    # ===== 文件上传区域 =====
    st.markdown("### 📤 上传新文档")
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
    st.caption("📌 系统状态：运行中 ✅")

# ===== 聊天区域 =====
# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天内容
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接受用户输入
if prompt := st.chat_input("请问您想问什么？"):
    # 显示用户的问题
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AI 正在检索知识库并思考中..."):
        try:
            response = ask(prompt)
        except Exception as e:
            response = f"【系统错误】后端调用失败，原因: {str(e)}"

    # 显示助手的回复
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# ===== 页脚 =====
st.divider()
st.caption("💡 基于 RAG 的数据结构知识问答系统 | 知识来源：《数据结构》教材")