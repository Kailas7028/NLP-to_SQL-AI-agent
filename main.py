from fastapi import FastAPI, HTTPException
from app.services.nlp_to_sql import run_agent
from app.api.schemas import QueryRequest
import uuid

app = FastAPI(title="NLP to SQL Agent")

@app.post("/query")
async def query_db(payload: QueryRequest):
    question = payload.question
    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    try:
        result = await run_agent(question)
        return {
            
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
