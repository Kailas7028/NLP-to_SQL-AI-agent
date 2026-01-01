from app.db.engine import engine
from sqlalchemy import text

def run_sql(sql: str):
    with engine.connect() as connection:
        # 1. Execute the SQL
        result = connection.execute(text(sql))
        
        # 2. Use .mappings() - This is the "Magic" step for SQLAlchemy 2.0
        # It automatically turns Rows into Dictionaries
        data = result.mappings().all()
        
        # 3. Convert to a standard list so FastAPI can read it
        return [dict(row) for row in data]