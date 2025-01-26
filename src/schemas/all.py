from pydantic import BaseModel, field_validator
from typing import List
from enum import Enum

class MessageType(str, Enum):
    AI = "AI"
    HUMAN = "HUMAN"

class DocumentType(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    TXT = "TXT"

class Message(BaseModel):
    message: str
    type: MessageType

class Item(BaseModel):
    query: str
    chat_history: List[Message]
    document_id: str
    
    @field_validator("query", "document_id")
    @classmethod
    def Item_validator(cls, v, field):
        if not v:
            raise ValueError(f"Invalid {field.field_name}")
        return v

class Document(BaseModel):
    document_id: str = ""
    description: str = ""
    path: str
    
    @field_validator("path")
    def check_document_type(cls, v):
        Ext = v.split(".")[-1].upper()
        if Ext not in DocumentType.__members__ or not v:
            raise ValueError("Invalid document type")
        return v
    
    