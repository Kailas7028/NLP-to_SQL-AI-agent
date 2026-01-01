from sqlalchemy import create_engine, text
import os

# Resolve DB path safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "sample.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

with engine.connect() as conn:
    # 1. Create table if it doesn't exist
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    """))

    # 2. Check if table already has data
    result = conn.execute(text("SELECT COUNT(*) FROM employees"))
    row_count = result.scalar()

    if row_count == 0:
        # 3. Seed data ONLY if table is empty
        conn.execute(text("""
            INSERT INTO employees (name, department, salary)
            VALUES
            ('Alice', 'HR', 60000),
            ('Bob', 'Engineering', 90000),
            ('Charlie', 'Finance', 70000),
            ('David', 'Engineering', 95000),
            ('Eva', 'HR', 65000),
            ('Frank', 'Finance', 72000)
        """))
        print("Seed data inserted.")
    else:
        print(f"Database already initialized with {row_count} rows. Skipping seed.")

    conn.commit()

print("Database initialization complete.")
