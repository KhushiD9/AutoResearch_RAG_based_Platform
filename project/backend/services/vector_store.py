import chromadb
from typing import List, Dict
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    """ChromaDB wrapper using the stable 0.4.x PersistentClient API."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        os.makedirs(persist_directory, exist_ok=True)
        try:
            self.client = chromadb.PersistentClient(path=persist_directory)
        except Exception:
            # Fallback to in-memory if persistence fails
            logger.warning("PersistentClient failed — falling back to EphemeralClient")
            self.client = chromadb.EphemeralClient()

    # ── collection helpers ─────────────────────────────────────────────────

    def get_or_create_collection(self, name: str):
        try:
            return self.client.get_or_create_collection(
                name=name,
                metadata={"description": "Research paper chunks"}
            )
        except Exception as e:
            logger.error(f"get_or_create_collection failed: {e}")
            return None

    # ── CRUD ───────────────────────────────────────────────────────────────

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str],
        embeddings: List[List[float]] = None
    ) -> bool:
        try:
            col = self.get_or_create_collection(collection_name)
            if col is None:
                return False

            kwargs = dict(documents=documents, metadatas=metadatas, ids=ids)
            if embeddings:
                kwargs["embeddings"] = embeddings

            col.add(**kwargs)
            return True
        except Exception as e:
            logger.error(f"add_documents failed: {e}")
            return False

    def query_documents(
        self,
        collection_name: str,
        query_texts: List[str] = None,
        query_embeddings: List[List[float]] = None,
        n_results: int = 5
    ) -> Dict:
        empty = {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        try:
            col = self.get_or_create_collection(collection_name)
            if col is None:
                return empty

            # Don't ask for more results than documents stored
            count = col.count()
            if count == 0:
                return empty
            n_results = min(n_results, count)

            if query_embeddings:
                return col.query(query_embeddings=query_embeddings, n_results=n_results)
            elif query_texts:
                return col.query(query_texts=query_texts, n_results=n_results)
            return empty
        except Exception as e:
            logger.error(f"query_documents failed: {e}")
            return empty

    def delete_collection(self, name: str) -> bool:
        try:
            self.client.delete_collection(name=name)
            return True
        except Exception as e:
            logger.error(f"delete_collection failed: {e}")
            return False

    def list_collections(self) -> List[str]:
        try:
            return [c.name for c in self.client.list_collections()]
        except Exception as e:
            logger.error(f"list_collections failed: {e}")
            return []
