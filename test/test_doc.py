import sys
from pathlib import Path


# 获取项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent

# 加入Python搜索路径
sys.path.append(str(ROOT_DIR))


from backend.models.document import Document



def test_document():

    doc = Document(
        document_id="001",
        filename="数据结构.pdf",
        filepath="data/documents/数据结构.pdf",
        file_type="pdf",
        course="数据结构",
        tags=[
            "树",
            "AVL"
        ]
    )


    print(doc)



if __name__ == "__main__":

    test_document()