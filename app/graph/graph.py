from langgraph.graph import StateGraph,END,START
from app.graph.state import State
from app.graph.nodes import embed_node,rag_query_node, generate_sql_node,validate_sql_node,run_sql_node


def should_continue(state:State)->str:
    if state.get("error") and state.get("retry_count",0) < 2:
        return "LLM"
    return END


def build_graph():
    workflow=StateGraph(state_schema=State)
    workflow.add_node("embed",embed_node)
    workflow.add_node("RAG",rag_query_node)
    workflow.add_node("LLM",generate_sql_node)
    workflow.add_node("validate",validate_sql_node)
    workflow.add_node("execute",run_sql_node)


    workflow.add_edge(START,"embed")
    workflow.add_edge("embed","RAG")
    workflow.add_edge("RAG","LLM")
    workflow.add_edge("LLM","validate")
    workflow.add_edge("validate","execute")
    workflow.add_conditional_edges("execute",should_continue,{"LLM":"LLM",END:END})
    # workflow.add_edge("final_result",END)

    return workflow.compile()

