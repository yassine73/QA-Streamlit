from fastapi import APIRouter
from src.schemas.all import Item, RawDocument
from dotenv import load_dotenv
import uuid
import logging

from src.services.weaviate import WeaviateService
from src.utils import refactor_chat_history

load_dotenv("config/.env")
logger = logging.getLogger(__name__)
chat_router = APIRouter()
client = WeaviateService()

@chat_router.post("/chat")
async def chat(item: Item):
    logger.info(f"Query: {item.query}")
    chat_history = refactor_chat_history(item.chat_history)
    
    
    return {"message": f"Hello your message is '{chat_history}'!"}

@chat_router.post("/add-document")
async def add_document(document: RawDocument):
    document.document_id = str(uuid.uuid4())
    return {"data": document.model_dump()}