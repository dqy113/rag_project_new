import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


from backend.document.manager import MetadataManager
from backend.models.document import Document



manager = MetadataManager()



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



manager.add_document(
    doc
)



documents = manager.get_all_documents()


for item in documents:

    print(item)