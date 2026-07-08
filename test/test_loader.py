import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


from backend.document.loader import DocumentLoader


loader = DocumentLoader()


doc = loader.load(
    "data/documents/深入理解计算机系统 (Randal E. Bryant, David R. O’Hallaron).pdf"
)


print(doc.document_id)

print(doc.filename)

print(len(doc.content))

print(doc.metadata)