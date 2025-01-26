import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
from weaviate.classes.query import Filter, MetadataQuery
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import os

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
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def load_data(self, path: str) -> List[Document]:
        ...
    
    def insert_data(self, docs: List[Document]) -> Tuple[int, str]:
        try:
            self.client.connect()
            collection = self.client.collections.get(os.getenv("WCD_COLLECTION"))
            for doc in docs:
                embedding = self.model.encode(doc.page_content).tolist()
                collection.data.insert(
                properties={
                    "file_name": doc.file_name,
                    "text": doc.page_content,
                    "parent_id": doc.document_id,
                },
                vector=embedding
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

    def vector_search(self, query: str, limit: int) -> Tuple[int, str]:
        return 200, "Vector search"