loader = DocumentLoader()

parser = DocumentParser()

splitter = DocumentSplitter()

embedding = EmbeddingModel()

chroma = ChromaManager()



document = loader.load(
    "data/AVL.pdf"
)



document = parser.parse(
    document
)



chunks = splitter.split(
    document
)



for chunk in chunks:

    chunk.embedding = (
        embedding.embed_text(
            chunk.content
        )
    )



chroma.add_chunks(
    chunks
)