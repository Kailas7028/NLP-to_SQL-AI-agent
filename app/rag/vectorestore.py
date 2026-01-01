#vectorstore.py
import chromadb
import uuid

class ChromaVectorStore:
    def __init__(
        self,path:str ="./chromadb", collection_name:str = "hrdb"):
        try:

            self.client= chromadb.PersistentClient(path=path)
            self.collection=self.client.get_or_create_collection(name=collection_name)
            self.documents=[]

        except Exception as e:
            raise(f"ChromaVectorStore class raised error client creation failed : {str(e)}")
    #-------------------------------------------------------------------------------------
    def is_empty(self,):
        return self.collection.count() == 0
    #--------------------------------------------------------------------------------------

    def add_vectors(
        self,
        documents:list[str],
        embeddings:list[list],
        metadata:list[dict] | None = None
    ):
            
        try:
                
            self.collection.upsert(
            ids=[str(uuid.uuid4()) for _ in range(len(documents))],
            embeddings=embeddings,
            documents=documents
            )

        except Exception as e:
            raise(f"ChromaVectorStore class raised error upserting failed : {str(e)}")
    #-------------------------------------------------------------------------------------------------

    
    def query(self,query_embeddings:list,top_k:int=2):
        try:
            return self.collection.query(
                query_embeddings=[query_embeddings],
                n_results=top_k
            )
        except Exception as e:
            raise(f"ChromaVectorStore class raised error query failed : {str(e)}")
    

