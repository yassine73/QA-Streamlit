from langchain_core.messages import HumanMessage, AIMessage
from typing import List
import logging

from src.schemas.all import Message, MessageType

logger = logging.getLogger(__name__)

def refactor_chat_history(chat_history: List[Message]) -> List[Message]:
    chat_holder = []
    logger.info(f"Chat history: {chat_history}")
    for message in chat_history:
        if message.type == MessageType.HUMAN:
            chat_holder.append(HumanMessage(content=message.message))
        elif message.type == MessageType.AI:
            chat_holder.append(AIMessage(content=message.message))
    logger.info(f"Refactored chat history: {chat_holder}")
    return chat_holder