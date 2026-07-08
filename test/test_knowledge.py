import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


from backend.document.loader import DocumentLoader
from backend.document.parser import DocumentParser
from backend.document.splitter import DocumentSplitter

from backend.vectorstore.embedding import EmbeddingModel
from backend.vectorstore.chroma_manager import ChromaManager

from backend.document.manager import MetadataManager

from backend.service.knowledge_service import KnowledgeService



# ==========================
# 初始化依赖
# ==========================

loader = DocumentLoader()

parser = DocumentParser()

splitter = DocumentSplitter(
    chunk_size=500,
    overlap=100
)


embedding = EmbeddingModel()


chroma = ChromaManager(
    persist_path="data/test_chroma_db"
)


metadata = MetadataManager(
    metadata_path="data/test_metadata/documents.json"
)



# ==========================
# 创建KnowledgeService
# ==========================

knowledge_service = KnowledgeService(

    loader=loader,

    parser=parser,

    splitter=splitter,

    embedding_model=embedding,

    chroma_manager=chroma,

    metadata_manager=metadata

)



# ==========================
# 测试上传
# ==========================


file_path = (
    "data/documents/"
    "深入理解计算机系统 (Randal E. Bryant, David R. O’Hallaron).pdf"
)



document = knowledge_service.add_document(

    file_path=file_path,

    course="计算机系统基础",

    tags=[
        "CSAPP",
        "程序链接",
        "内存"
    ]

)



print("\n==========上传结果==========")

print(document)



# ==========================
# 测试metadata
# ==========================


print("\n==========Metadata==========")

documents = (
    knowledge_service
    .get_documents()
)


for doc in documents:

    print(doc)



# ==========================
# 测试Chroma数量
# ==========================


print("\n==========Chroma==========")

print(
    "chunk数量:",
    chroma.count()
)