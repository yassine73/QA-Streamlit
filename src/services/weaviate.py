import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
from weaviate.classes.query import Filter, MetadataQuery
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Tuple
import copy
import os

from src.handlers.embeddings import EMBEDDINGS
from src.schemas.all import RawDocument, DocumentType

class WeaviateService:
    def __init__(self):
        # self.client = weaviate.WeaviateClient(
        #     connection_params=ConnectionParams.from_params(
        #         http_host=os.getenv("WCD_URL"),
        #         http_port=8080,
        #         http_secure=True,
        #         grpc_host=os.getenv("WCD_gRPC"),
        #         grpc_port=50051,
        #         grpc_secure=True,
        #     ),
        #     auth_client_secret=Auth.api_key(os.getenv("WCD_API_KEY")),
        #     additional_config=AdditionalConfig(
        #         timeout=Timeout(init=30, query=30, insert=60),
        #     ),
        # )
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("WCD_URL"),
            auth_credentials=Auth.api_key(os.getenv("WCD_API_KEY")),
            additional_config=AdditionalConfig(
                timeout=Timeout(init=30, query=30, insert=60),
            ),
        )
        self.model = EMBEDDINGS()
    
    def load_data(self, raw_document: RawDocument) -> List[Document]:
        if raw_document.document_type == DocumentType.PDF:
            loader = PyPDFLoader(raw_document.path)
        elif raw_document.document_type == DocumentType.DOCX:
            loader = Docx2txtLoader(raw_document.path)
        elif raw_document.document_type == DocumentType.TXT:
            loader = TextLoader(raw_document.path)
        
        metadata = {
            "file_name": raw_document.path.split("/")[-1],
            "document_id": raw_document.document_id,
            "description": raw_document.description,
            "path": raw_document.path,
        }
        docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100))
        for doc in docs:
            _metadata = copy.deepcopy(metadata)
            if doc.page_number:
                _metadata["page_number"] = doc.page_number + 1
            doc.metadata = _metadata
        return docs
    
    def insert_data(self, docs: List[Document]) -> Tuple[int, str]:
        try:
            self.client.connect()
            collection = self.client.collections.get(os.getenv("WCD_COLLECTION"))
            for doc in docs:
                collection.data.insert(
                properties={
                    "metadata": doc.metadata,
                    "text": doc.page_content
                },
                vector=self.model.embed_query(doc.page_content)
            )
        except Exception as e:
            return 400, str(e)
        finally:
            self.client.close()
        return 200, "Data inserted"
    
    def delete_documents(self, doc_id: str) -> Tuple[int, str]:
        try:
            self.client.connect()
            collection = self.client.collections.get(os.getenv("WCD_COLLECTION"))
            collection.data.delete_many(
                where=Filter.by_property("parent_id").equal(doc_id)
            )
        except Exception as e:
            return 400, str(e)
        finally:
            self.client.close()
        return 200, "Documents deleted"

    def vector_search(self, query: str, limit: int, doc_id: str) -> Tuple[int, any]:
        try:
            self.client.connect()
            collection = self.client.collections.get(os.getenv("WCD_COLLECTION"))
            query_embed = self.model.embed_query(query)
            result = collection.query.near_vector(
                near_vector=query_embed,
                limit=limit,
                return_metadata=MetadataQuery(distance=True),
                filters=Filter.by_property("parent_id").equal(doc_id)
            )
            
            relevant_docs = []
            for doc in result.objects:
                relevant_docs.append(Document(
                    page_content=doc.properties['text'],
                    metadata=doc.properties['metadata']
                ))
                
        except Exception as e:
            return 400, str(e)
        finally:
            self.client.close()
        return 200, relevant_docs