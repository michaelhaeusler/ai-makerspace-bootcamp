"""Vector storage service for policy chunks and embeddings."""

import uuid
from typing import Dict, List, Optional

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue

from app.core.config import VectorStoreConfig, settings


class VectorStore:
    """Handles vector storage and retrieval for policy chunks."""
    
    def __init__(self, config: VectorStoreConfig):
        """Initialize vector store with configuration."""
        self.config = config
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None
        )
    
    def create_policy_collection(self, policy_id: str) -> str:
        """
        Create a new Qdrant collection for a specific policy.
        
        Args:
            policy_id: Unique identifier for the policy
            
        Returns:
            Collection name
        """
        collection_name = f"{self.config.collection_prefix}{policy_id}"
        
        # Check if collection exists, delete if it does
        if self.qdrant_client.collection_exists(collection_name):
            self.qdrant_client.delete_collection(collection_name)
        
        # Create new collection
        self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI text-embedding-3-small dimension
                distance=Distance.COSINE
            )
        )
        
        return collection_name
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        response = self.openai_client.embeddings.create(
            model=self.config.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def store_chunks(self, policy_id: str, chunks: List[Dict]) -> Dict:
        """
        Store policy chunks in Qdrant with embeddings.
        
        Args:
            policy_id: Unique identifier for the policy
            chunks: List of chunk dictionaries from PDFProcessor
            
        Returns:
            Dictionary with storage results
        """
        collection_name = self.create_policy_collection(policy_id)
        points = []
        
        for chunk in chunks:
            # Generate embedding for chunk text
            embedding = self.embed_text(chunk["text"])
            
            # Create point for Qdrant
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "page": chunk["page"],
                    "filename": chunk["filename"],
                    "upload_date": chunk["upload_date"],
                    "token_count": chunk["token_count"],
                    "policy_id": policy_id
                }
            )
            points.append(point)
        
        # Store all points in Qdrant
        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        return {
            "collection_name": collection_name,
            "points_stored": len(points),
            "policy_id": policy_id
        }
    
    def search_similar_chunks(self, policy_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Search for similar chunks in a policy collection.
        
        Args:
            policy_id: Policy to search in
            query: Search query text
            limit: Maximum number of results (uses config default if None)
            
        Returns:
            List of similar chunks with scores
        """
        collection_name = f"{self.config.collection_prefix}{policy_id}"
        
        if not self.qdrant_client.collection_exists(collection_name):
            return []
        
        # Generate embedding for query
        query_embedding = self.embed_text(query)
        
        # Search in Qdrant
        results = self.qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit or self.config.max_results,
            score_threshold=self.config.similarity_threshold
        )
        
        # Format results
        similar_chunks = []
        for result in results:
            similar_chunks.append({
                "chunk_id": result.payload["chunk_id"],
                "text": result.payload["text"],
                "page": result.payload["page"],
                "filename": result.payload["filename"],
                "score": result.score,
                "metadata": {
                    "token_count": result.payload["token_count"],
                    "upload_date": result.payload["upload_date"]
                }
            })
        
        return similar_chunks
    
    def delete_policy(self, policy_id: str) -> bool:
        """
        Delete all chunks for a specific policy.
        
        Args:
            policy_id: Policy to delete
            
        Returns:
            True if successful
        """
        collection_name = f"{self.config.collection_prefix}{policy_id}"
        
        if self.qdrant_client.collection_exists(collection_name):
            self.qdrant_client.delete_collection(collection_name)
            return True
        
        return False
