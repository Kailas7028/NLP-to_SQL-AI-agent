#function utility
import re
from sqlalchemy import text,inspect


    #Extracting sql from llm result
def extract_sql(text: str) -> str:
    # remove markdown fences
    text = re.sub(r"```sql|```", "", text, flags=re.IGNORECASE).strip()
    
    # find first SELECT till end
    match = re.search(
        r"(SELECT[\s\S]+)",
        text,
        re.IGNORECASE
    )
    
    if not match:
        raise ValueError(f"No SQL found in LLM output:\n{text}")
    
    sql = match.group(1).strip()
    
    # cut off anything after last ')'
    sql = sql.split("\n\n")[0]
    
    # ensure semicolon
    if not sql.endswith(";"):
        sql += ";"
    
    return sql


    #fetching schema
def get_schema(engine):
    inspector=inspect(engine)
    schema={}
    for table in inspector.get_table_names():
        cols= inspector.get_columns(table)
        schema[table]=[col["name"] for col in cols]
        
    return schema


    #question embedding
def embed_question(embedder, question: str):
    return embedder.embed([question])[0]


   



    #rag result pruning
def prune(retrieved_docs: list[str]) -> dict[str, list[str]]:
    """
    Extract only tables & columns mentioned in retrieved schema docs
    """
    pruned_schema = {}

    for doc in retrieved_docs:
        lines = doc.splitlines()
        table = None

        for line in lines:
            if line.lower().startswith("table:"):
                table = line.split(":")[1].strip()
                pruned_schema[table] = []

            elif line.startswith("-") and table:
                col = line.replace("-", "").strip()
                pruned_schema[table].append(col)

    return pruned_schema



    #formating retrived schema
def format_schema_for_prompt(schema: dict[str, list[str]]) -> str:
    lines = []
    for table, cols in schema.items():
        cols_str = ", ".join(cols)
        lines.append(f"{table}({cols_str})")
    return "\n".join(lines)

#validate sql
def block_unsafe_sql(sql:str):
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
    
    for word in forbidden:
        if word in sql.lower():
            raise ValueError("Unsafe SQL detected")