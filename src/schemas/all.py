from pydantic import BaseModel, field_validator
from typing import List, Optional
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

class RawDocument(BaseModel):
    document_id: Optional[str] = None
    description: Optional[str] = None
    path: str
    
    @field_validator("path")
    @classmethod
    def Document_validator(cls, v):
        if v not in list(DocumentType.__members__):
            raise ValueError(f"Invalid file type")
        return v
    
    @property
    def document_type(self):
        Ext: DocumentType = self.path.split(".")[-1].upper()
        return DocumentType(Ext)
    