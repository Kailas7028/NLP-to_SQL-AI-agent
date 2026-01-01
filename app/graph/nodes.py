from app.core.container import embedder,vector_store,llm,schema
from app.logger.logger import get_logger
from app.graph.state import State
from app.tools.utils import prune,format_schema_for_prompt,extract_sql,block_unsafe_sql
from app.prompts.prompts import build_prompt,build_summary_prompt
from app.db.executor import run_sql
from app.validators.sql_validator import SQLSchemaValidator


logger=get_logger("AISQL")

#node embedding
def embed_node(state:State)->State:
    embedings=embedder.embed([state["question"]])[0]
    return {
        "question_embedding":embedings
    }

#node rag retriveal
def rag_query_node(state:State)->State:
    rag_schema=vector_store.query(state["question_embedding"])
    docs=rag_schema["documents"][0]
    pruned_schema=prune(docs)
    formated_schema=format_schema_for_prompt(pruned_schema)
    return{
        "retrieved_schema":formated_schema 
    }

#node sql generation
async def generate_sql_node(state:State)->State:

    if state.get("error"):
        if state.get("retry_count", 0) >= 2:
            return {"error": "Max retries exceeded"}
        else:
            prompt=f"""The previous SQL failed with this error: {state['error']}. 
            Fix the SQL for the question: {state['question']} 
            using this schema: {state['retrieved_schema']}"""
    else:
        prompt= build_prompt(state["question"],state["retrieved_schema"])

    response=await llm.generate(prompt)
    return {
        "response":response
    }


#node validate
def validate_sql_node(state:State)->State:
    try:
        sql=extract_sql(state["response"])
        block_unsafe_sql(sql)
        validator=SQLSchemaValidator(schema)
        validator.validate(sql)
        return{
            "sql":sql
        }
    except Exception as e:
        raise(e)

#node run sql
async def run_sql_node(state:State)->State:
    retry_count=state.get("retry_count",0)
    try:
        result=run_sql(state["sql"])
        summary_prompt=build_summary_prompt(state["question"],result)
        summary_response=await llm.generate(summary_prompt)
        return{
            "summary":summary_response
        }
    except Exception as e:
        return{
            "error": str(e),
            "retry_count":retry_count + 1
        }

    
