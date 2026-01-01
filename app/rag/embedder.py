#embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np


class SchemaEmbedder:
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
   
    def embed(self, documents: list[str]) -> np.ndarray:
        """
        Generate embeddings for schema documents.
        """
        
        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True
        )
        return embeddings
        
