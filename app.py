import streamlit as st
import os
from backend.rag import ask

st.set_page_config(page_title="智能问答助手", page_icon="🤖")
st.title("🤖 我的第一个智能问答网页")

with st.sidebar:
    st.markdown("## 📚 知识库管理")
    
   # 动态显示知识库状态：读取 data/ 文件夹里的文档数量
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
        accept_multiple_files=True,  # 支持批量上传
        label_visibility="collapsed"  # 隐藏默认标签
    )
    
    # 处理上传的文件
    if uploaded_files:
        for file in uploaded_files:
            # 显示每个文件的上传状态
            with st.spinner(f"⏳ 正在处理：{file.name}..."):
                # TODO: 这里调用后端的解析和入库函数
                # 目前先模拟处理成功
                pass
        
        # 全部上传完成后显示成功消息
        st.success(f"✅ 成功上传 {len(uploaded_files)} 个文件！")
        
        # TODO: 刷新知识库状态
        # st.rerun()  # 可以取消注释，自动刷新页面

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