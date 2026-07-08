import uuid

from backend.models.document import Document
from backend.models.chunk import Chunk
from backend.utils.logger import logger



class DocumentSplitter:


    def __init__(
        self,
        chunk_size:int=500,
        overlap:int=100
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap



    def split(
        self,
        document:Document
    )->list[Chunk]:


        chunks=[]


        index=0


        # PDF页级切分

        if "pages" in document.metadata:


            for page in document.metadata["pages"]:

                chunks.extend(
                    self.split_text(
                        document,
                        page["content"],
                        {
                            "page":page["page"]
                        },
                        index
                    )
                )

                index += len(chunks)



        else:

            chunks.extend(
                self.split_text(
                    document,
                    document.content,
                    {},
                    index
                )
            )



        logger.info(
            f"{document.filename} split into {len(chunks)} chunks"
        )


        return chunks




    def split_text(
        self,
        document,
        text,
        extra_metadata,
        start_index
    ):


        chunks=[]


        start=0


        index=start_index


        while start < len(text):


            end=start+self.chunk_size


            chunk_text=text[start:end]


            chunk=Chunk(

                id=str(uuid.uuid4()),

                document_id=document.id,

                content=chunk_text,

                metadata={

                    "source":
                    document.filename,


                    "type":
                    document.file_type,


                    "chunk_index":
                    index,


                    **extra_metadata

                }

            )


            chunks.append(chunk)


            index+=1


            start=end-self.overlap


        return chunks