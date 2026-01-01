def build_prompt(question: str, schema_text: str) -> str:
    """
    Builds a few-shot prompt to guide GPT-4o-mini in generating accurate SQL.
    """
    
    # 1. Define few-shot examples (Replace these with examples from your actual DB)
    examples = """
-- Examples:
-- Question: Who are the employees in HR?
-- SQL: SELECT name FROM employees WHERE department = 'HR';

-- Question: What is the average salary in the Engineering department?
-- SQL: SELECT AVG(salary) FROM employees WHERE department = 'Engineering';

-- Question: List the top 3 highest paid employees.
-- SQL: SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;
"""

    # 2. Construct the final prompt
    return f"""TASK: You are a SQL expert. Generate a valid SQL SELECT statement for SQLite based on the SCHEMA provided below.

SCHEMA:
{schema_text}

{examples}

RULES:
- Output ONLY the raw SQL code.
- Do NOT include markdown code blocks (like ```sql).
- Do NOT provide explanations or commentary.
- Use only the tables and columns listed in the SCHEMA.
- Ensure the query is compatible with SQLite.

QUESTION: 
{question}

SQL:"""




def build_summary_prompt(question: str, sql_results: list) -> str:
    return f"""
    TASK: Summarize the database results in natural language.
    
    USER QUESTION: {question}
    DATABASE DATA: {sql_results}
    
    INSTRUCTIONS:
    - Provide a concise, helpful summary.
    - If no data was found, politely say so.
    - Do not mention table names or internal IDs unless relevant.
    
    SUMMARY:
    """