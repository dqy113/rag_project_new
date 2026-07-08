import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


from backend.document.loader import DocumentLoader
from backend.document.parser import DocumentParser
from backend.document.splitter import DocumentSplitter



loader = DocumentLoader()

parser = DocumentParser()

splitter = DocumentSplitter(
    chunk_size=500,
    overlap=100
)


doc = loader.load(
    "data/documents/chapter1.pdf"
)


doc = parser.parse(
    doc
)


chunks = splitter.split(
    doc
)


print(
    "chunk数量:",
    len(chunks)
)


print(
    chunks[0]
)