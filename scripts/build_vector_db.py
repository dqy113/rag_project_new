from pathlib import Path

from backend.document.loader import DocumentLoader
from backend.document.parser import DocumentParser
from backend.document.splitter import DocumentSplitter

from backend.vectorstore.embedding import EmbeddingModel
from backend.vectorstore.chroma_manager import ChromaManager


DATA_DIR = Path(
    "data/documents"
)

CHROMA_PATH = (
    "data/chroma_db"
)

COLLECTION_NAME = (
    "knowledge_base"
)


loader = DocumentLoader()

parser = DocumentParser()

splitter = DocumentSplitter()

embedding = EmbeddingModel()

chroma = ChromaManager(
    persist_path=CHROMA_PATH,
    collection_name=COLLECTION_NAME
)



def build_vector_db():

    files = [
        file
        for file in DATA_DIR.iterdir()
        if file.suffix.lower() in [
            ".pdf",
            ".txt",
            ".docx",
            ".pptx"
        ]
    ]


    print(
        "发现文件数量:",
        len(files)
    )


    total_chunks = 0


    for file in files:

        print(
            "\n处理文件:",
            file.name
        )


        document = loader.load(
            str(file)
        )


        print(
            "Loader文本长度:",
            len(document.content)
        )


        document = parser.parse(
            document
        )


        print(
            "Parser文本长度:",
            len(document.content)
        )


        chunks = splitter.split(
            document
        )


        print(
            "生成Chunk数量:",
            len(chunks)
        )


        if len(chunks) == 0:
            print(
                "没有生成chunk，跳过"
            )
            continue



        for index, chunk in enumerate(chunks):

            vector = embedding.embed_text(
                chunk.content
            )


            if len(vector) == 0:
                print(
                    "Embedding为空:",
                    index
                )


            chunk.embedding = vector


            chunk.metadata["document_id"] = (
                document.id
            )


        chroma.add_chunks(
            chunks
        )


        total_chunks += len(chunks)


        print(
            "写入Chunk:",
            len(chunks)
        )



    print(
        "\n===================="
    )

    print(
        "总写入Chunk:",
        total_chunks
    )


    print(
        "Chroma当前数量:",
        chroma.count()
    )


    print(
        "知识库构建完成"
    )



if __name__ == "__main__":

    build_vector_db()