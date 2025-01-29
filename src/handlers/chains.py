from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from typing import List

from src.constants.prompts import SYSTEM_TEMPLATE
from src.schemas.all import Message

class Chains:
    def __init__(self, chat_history: List[Message], model: BaseLanguageModel):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_TEMPLATE),
            MessagesPlaceholder("chat_history"),
            ("human", "{query}")
        ])
        self.rag_chain = prompt | model | StrOutputParser()
        self.rag_chain.name = "RAG Chain"