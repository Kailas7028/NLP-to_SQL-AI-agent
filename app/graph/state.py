from typing import TypedDict,Optional,List


class State(TypedDict):
    question:str
    question_embedding:Optional[list[float]]
    retrieved_schema:list[str]
    response:str
    sql:str
    summary:str
    error:Optional[str]
    retry_count:int