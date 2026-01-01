# NLP to SQL Agent (Schema-Aware, RAG-Based)

An end-to-end **Natural Language to SQL** system that allows users to query a relational database using plain English.  
The system uses **schema-aware retrieval (RAG)**, **LLM-based SQL generation**, and **LangGraph orchestration** with validation and retry logic.

This project is designed as a **multi-user async API**, focusing on correctness, safety, and extensibility rather than prompt-only SQL generation.

---

## ✨ Key Features

- 🧠 **Schema-Aware RAG**
  - Database schema is embedded and stored in a vector database (ChromaDB)
  - Only relevant tables & columns are exposed to the LLM

- 🔁 **Iterative SQL Repair**
  - SQL execution errors are fed back to the LLM
  - Automatic retries using LangGraph conditional routing

- 🛡️ **SQL Safety Validation**
  - Blocks unsafe queries (`DROP`, `DELETE`, `UPDATE`, etc.)
  - Read-only query enforcement

- ⚡ **Async, Multi-user API**
  - Built using FastAPI + async LLM calls
  - Shared resources (LLM, embeddings, vector store) loaded once

- 🧩 **Modular & Extensible Design**
  - Clear separation of concerns
  - Easy to add new validators, databases, or LLMs

---

## 🏗️ Architecture Overview

**High-level flow:**

User Question
↓
Question Embedding
↓
Schema Retrieval (ChromaDB)
↓
Schema Pruning
↓
LLM SQL Generation
↓
SQL Validation
↓
SQL Execution
↓
Result Summarization


**Core technologies used:**
- FastAPI
- LangGraph
- LangChain (ChatOpenAI)
- ChromaDB
- SentenceTransformers
- SQLAlchemy (SQLite)

---

NLP_TO_SQL/
├── app/
│   ├── api/          # Request/response schemas
│   ├── core/         # Dependency container
│   ├── db/           # DB engine & executor
│   ├── graph/        # LangGraph state machine
│   ├── llm/          # LLM client abstraction
│   ├── rag/          # Schema documents, embeddings, vector store
│   ├── prompts/      # Prompt templates
│   ├── services/     # High-level agent service
│   ├── tools/        # Utilities (SQL parsing, schema utils)
│   └── logger/       # Structured JSON logging
├── init_db.py         # Database initialization (run once)
├── main.py            # FastAPI entrypoint
├── .env.example       # Environment variable template
├── .gitignore
└── README.md





---

## ⚙️ Environment Setup

### 1️⃣ Clone the repository
```bash
git clone <repo-url>
cd NLP_TO_SQL

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables
Create .env from template:
cp .env.example .env
Update .env:
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini

🗄️ Database Initialization
Run once to create and seed the database:
python init_db.py

The script:

Creates tables if they don’t exist

Inserts sample data only if the table is empty

Prevents data duplication on re-runs

🚀 Running the API
uvicorn main:app --reload

API will be available at:
http://localhost:8000

🔍 Example API Usage
Endpoint
POST /query

Request
{
  "question": "What is the average salary in Engineering?"
}

Response
{
  "result": {
    "question": "What is the average salary in Engineering?",
    "sql": "SELECT AVG(salary) FROM employees WHERE department = 'Engineering';",
    "answer": "The average salary in the Engineering department is 90,000."
  }
}

🧪 Error Handling & Retries

SQL execution failures are captured

Error message is fed back to the LLM

Query is regenerated (up to 2 retries)

Controlled using LangGraph conditional edges

🧠 Design Decisions
Why Schema RAG?

Prevents hallucinated tables/columns

Reduces token usage

Improves SQL correctness

Why LangGraph?

Explicit state transitions

Deterministic retry logic

Easier debugging vs linear chains

Why Shared Resources?

Embeddings, schema, and vector store are loaded once

Supports concurrent users efficiently

🚧 Known Limitations / Future Improvements

SQL parser-based validation (planned)

Column-level semantic validation

Support for JOIN-heavy queries

Pagination & large result handling

Support for PostgreSQL / MySQL

Authentication & rate limiting

👨‍💻 Author

Kailas
AI Engineer | Conversational AI | NLP → SQL Systems
Focused on building robust, production-ready AI agents

📜 License

This project is for learning, evaluation, and demonstration purposes.
