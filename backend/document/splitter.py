from langchain_text_splitters import RecursiveCharacterTextSplitter

# 分块参数不变
def split_text(doc_list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    all_chunks = []
    # 遍历每一页文档，单独分块，保留来源、页码信息
    for doc in doc_list:
        pieces = splitter.split_text(doc["content"])
        for piece in pieces:
            all_chunks.append({
                "text": piece,
                "source_file": doc["source"],
                "page_num": doc["page"]
            })
    return all_chunks