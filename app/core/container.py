# app/core/container.py

from app.db.engine import engine
from app.tools.utils import get_schema
from app.rag.documents import Documents
from app.rag.embedder import SchemaEmbedder
from app.rag.vectorestore import ChromaVectorStore
from app.llm.client import GPT4Client
from app.config import MODEL_NAME


vector_store = ChromaVectorStore()
# 1. Load schema ONCE
schema = get_schema(engine)

# 3. Load embedder ONCE
embedder = SchemaEmbedder()


# 6. Load LLM ONCE
llm = GPT4Client(MODEL_NAME)

if vector_store.is_empty():

    # 2. Build schema documents ONCE
    doc_builder = Documents()
    doc_builder.build_documents(schema)
    schema_documents = doc_builder.documents


    # 4. Embed schema ONCE
    schema_embeddings = embedder.embed(schema_documents)

    # 5. Vector store ONCE
   
    vector_store.add_vectors(schema_documents, schema_embeddings)


