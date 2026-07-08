# backend/vectorstore/chroma_manager.py

import chromadb

from backend.models.chunk import Chunk
from backend.utils.logger import logger



class ChromaManager:
    """
    Chroma向量数据库管理器

    负责:
    1. 创建collection
    2. 保存Chunk
    3. 向量搜索
    4. 删除知识
    """


    def __init__(
        self,
        persist_path="data/chroma_db",
        collection_name="knowledge_base"
    ):

        self.persist_path = persist_path

        self.collection_name = collection_name


        logger.info(
            f"Initialize Chroma: {persist_path}"
        )


        self.client = (
            chromadb.PersistentClient(
                path=persist_path
            )
        )


        # 不存在则创建
        self.collection = (
            self.client
            .get_or_create_collection(
                name=collection_name
            )
        )


        logger.info(
            f"Collection ready: {collection_name}"
        )



    def add_chunks(
        self,
        chunks:list[Chunk]
    ):
        """
        将Chunk写入Chroma

        输入:
            Chunk列表
        """


        ids = []

        documents = []

        embeddings = []

        metadatas = []


        for chunk in chunks:

            ids.append(
                chunk.id
            )

            documents.append(
                chunk.content
            )

            embeddings.append(
                chunk.embedding
            )

            metadatas.append(
                chunk.metadata
            )


        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )


        logger.info(
            f"Inserted {len(chunks)} chunks"
        )



    def similarity_search(
        self,
        query_vector:list[float],
        top_k:int=5
    )->list[Chunk]:
        """
        根据问题向量搜索

        输入:
            query_vector

        输出:
            Chunk列表
        """


        result = (
            self.collection
            .query(
                query_embeddings=[
                    query_vector
                ],

                n_results=top_k
            )
        )


        chunks=[]


        docs = result["documents"][0]

        ids = result["ids"][0]

        metadatas = result["metadatas"][0]



        for i in range(len(docs)):

            chunk = Chunk(

                id=ids[i],

                document_id=
                metadatas[i].get(
                    "document_id",
                    ""
                ),

                content=docs[i],

                metadata=metadatas[i]

            )


            chunks.append(
                chunk
            )


        return chunks



    def delete_by_source(
        self,
        source:str
    ):
        """
        删除某个文件产生的所有Chunk
        """

        self.collection.delete(
            where={
                "source":source
            }
        )

    def delete_by_document_id(
    self,
    document_id:str
    ):
        """
        根据document_id删除整个文档产生的chunk
        """

        self.collection.delete(
            where={
                "document_id": document_id
            }
    )

    def clear(self):
        """
        清空当前知识库

        重建数据库时使用
        """


        self.client.delete_collection(
            self.collection_name
        )


        self.collection = (
            self.client
            .get_or_create_collection(
                name=self.collection_name
            )
        )



    def count(self):

        return (
            self.collection.count()
        )