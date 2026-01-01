from langchain_openai import ChatOpenAI

class LLMClient:
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError
    


class GPT4Client(LLMClient):
    def __init__(self, model_name: str):
        self.model = ChatOpenAI(model=model_name, temperature=0)

    async def generate(self, prompt: str) -> str:
        try:
            # Using ainvoke for non-blocking I/O
            response = await self.model.ainvoke(prompt)
            return response.content
        except Exception as e:
            raise(f"LLM las raised error: {str(e)}")