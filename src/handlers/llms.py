from langchain_groq import ChatGroq

class LLM:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            timeout=30
        )