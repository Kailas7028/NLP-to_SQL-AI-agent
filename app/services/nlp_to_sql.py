
from app.graph.graph import build_graph

graph=build_graph()

async def run_agent(question:str):
    
    initial_state={
        "question":question,
        "retry_count": 0 
        }

    result=await graph.ainvoke(initial_state)

    return{
        "question":question,
        "sql":result["sql"],
        "answer":result["summary"]

    }