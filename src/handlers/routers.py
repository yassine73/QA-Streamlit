from fastapi import APIRouter
from src.schemas.all import Item, Document
from dotenv import load_dotenv
import uuid

load_dotenv("config/.env")
from src.services.weaviate import WeaviateService

chat_router = APIRouter()
client = WeaviateService()

@chat_router.post("/chat")
async def chat(item: Item):
    return {"message": f"Hello your message is '{item.query}'!"}

@chat_router.post("/add-document")
async def add_document(document: Document):
    document.document_id = str(uuid.uuid4())
    return {"message": f"Hello your message is '{document.document_id}'!"}