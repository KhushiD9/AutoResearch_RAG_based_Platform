from typing import List
import logging
import numpy as np

logger = logging.getLogger(__name__)

_model = None

def _get_model():
    """Lazy-load sentence-transformers model (loads once, reused on every call)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading sentence-transformer model all-MiniLM-L6-v2 ...")
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Model loaded.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer: {e}")
            raise
    return _model


class EmbeddingService:
    """Free local embeddings via sentence-transformers (all-MiniLM-L6-v2, 384-dim)."""

    def __init__(self, provider: str = "local"):
        # provider param kept for API compatibility — always uses local model
        self.provider = provider

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Batch-encode a list of texts and return embeddings as plain lists."""
        if not texts:
            return []
        try:
            model = _get_model()
            embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

    async def generate_query_embedding(self, query: str) -> List[float]:
        """Encode a single query string."""
        results = await self.generate_embeddings([query])
        return results[0] if results else []
