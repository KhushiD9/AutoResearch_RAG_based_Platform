import chromadb
from chromadb.config import Settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collection_name = "research_papers"
        
    def get_or_create_collection(self, collection_name: str = None):
        """Get or create a ChromaDB collection"""
        if collection_name is None:
            collection_name = self.collection_name
            
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Research paper chunks"}
            )
            return collection
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return None
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str],
        embeddings: List[List[float]] = None
    ):
        """Add documents to the vector store"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            if embeddings:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
            else:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    def query_documents(
        self,
        collection_name: str,
        query_texts: List[str] = None,
        query_embeddings: List[List[float]] = None,
        n_results: int = 5
    ) -> Dict:
        """Query the vector store"""
        try:
            collection = self.get_or_create_collection(collection_name)
            
            if query_embeddings:
                results = collection.query(
                    query_embeddings=query_embeddings,
                    n_results=n_results
                )
            elif query_texts:
                results = collection.query(
                    query_texts=query_texts,
                    n_results=n_results
                )
            else:
                return {"documents": [], "metadatas": [], "distances": []}
            
            return results
        except Exception as e:
            logger.error(f"Error querying documents: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        try:
            self.client.delete_collection(name=collection_name)
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False
    
    def list_collections(self) -> List[str]:
        """List all collections"""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []
