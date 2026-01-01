#documents.py
from sqlalchemy import inspect
class Documents:
    def __init__(self,):
        self.documents:list[str]=[]
        

    
    def build_documents(self,schema):
        """
        Convert DB schema into retrievable text documents.
        One document per table.
        """
        try: 
        
            for table, columns in schema.items():
                doc_lines = [
                    f"Table: {table}",
                    "Columns:"
                ]
        
                for col in columns:
                    doc_lines.append(f"- {col}")
        
                self.documents.append("\n".join(doc_lines))
        except Exception as e:
            raise(f"Documents class raised error: {str(e)}")