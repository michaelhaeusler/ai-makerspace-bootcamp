import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio
import logging
import time


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)


class VectorDatabase:
    def __init__(
        self, embedding_model: EmbeddingModel = None, enable_logging: bool = True
    ):
        """
        Initialize VectorDatabase with optional logging.

        Args:
            embedding_model: EmbeddingModel instance for creating embeddings
        """
        self.vectors = defaultdict(np.array)

        # Create embedding model with matching logging preference
        self.embedding_model = embedding_model or EmbeddingModel(
            enable_logging=enable_logging
        )
        self.enable_logging = enable_logging

        # Set up logging using the same pattern as EmbeddingModel
        if self.enable_logging:
            # Create logger with hierarchical name
            self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

            # Don't create handlers - let the root logger handle it
            self.logger.propagate = True

    def insert(self, key: str, vector: np.array) -> None:
        self.vectors[key] = vector

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
    ) -> List[Tuple[str, float]]:
        """
        Search for the k most similar vectors using the specified distance measure.

        Args:
            query_vector: The query vector to search for
            k: Number of top results to return
            distance_measure: Function to calculate similarity (default: cosine_similarity)

        Returns:
            List of tuples (text, similarity_score) sorted by similarity (highest first)
        """
        # Log search initiation with key parameters
        if self.enable_logging:
            self.logger.info(
                f"Searching for top {k} similar vectors from {len(self.vectors)} total vectors"
            )

        # Start timing the search operation
        start_time = time.time()

        # Calculate scores for all vectors, sort them by similarity in descending order and return the top k results
        scores = [
            (key, distance_measure(query_vector, vector))
            for key, vector in self.vectors.items()
        ]
        results = sorted(scores, key=lambda x: x[1], reverse=True)[:k]

        # Log search completion and performance metrics
        if self.enable_logging:
            elapsed = time.time() - start_time
            self.logger.info(f"Search completed in {elapsed:.3f}s")

        # Log search quality metrics
        if results:
            self.logger.info(f"Top similarity score: {results[0][1]:.3f}")
            if len(results) > 1:
                self.logger.debug(
                    f"Score range: {results[0][1]:.3f} to {results[-1][1]:.3f}"
                )
        else:
            self.logger.warning("No results found in search")

        return results

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
    ) -> List[Tuple[str, float]]:
        """
        Search for similar vectors using text query.

        Args:
            query_text: Text to search for
            k: Number of top results to return
            distance_measure: Function to calculate similarity
            return_as_text: If True, return only text without scores

        Returns:
            List of tuples (text, similarity_score) or just texts if return_as_text=True
        """
        # Log the search query (truncate long queries for readability)
        if self.enable_logging:
            query_preview = (
                query_text[:50] + "..." if len(query_text) > 50 else query_text
            )
            self.logger.info(f"Searching by text: '{query_preview}'")

        # Start timing the entire text search operation
        start_time = time.time()

        # Create embedding for the query text (this calls the embedding API)
        query_vector = self.embedding_model.get_embedding(query_text)

        # Log embedding creation time
        if self.enable_logging:
            embedding_time = time.time() - start_time
            self.logger.info(f"Query embedding created in {embedding_time:.3f}s")

        # Perform vector search using the embedded query
        results = self.search(query_vector, k, distance_measure)

        # Log total operation time
        if self.enable_logging:
            total_time = time.time() - start_time
            self.logger.info(f"Total text search completed in {total_time:.3f}s")

        # Return results in requested format
        return [result[0] for result in results] if return_as_text else results

    def retrieve_from_key(self, key: str) -> np.array:
        return self.vectors.get(key, None)

    async def abuild_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        """
        Build vector database from a list of texts with comprehensive logging.

        Args:
            list_of_text: List of text strings to create embeddings for

        Returns:
            Self (for method chaining)
        """
        # Log the database building operation start
        if self.enable_logging:
            self.logger.info(f"Building vector database from {len(list_of_text)} texts")

        # Start timing the entire database building process
        start_time = time.time()

        # Get embeddings (this will show progress bar if enabled in EmbeddingModel)
        # The EmbeddingModel will handle its own logging and progress tracking
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)

        # Log the transition from embedding creation to database insertion
        if self.enable_logging:
            self.logger.info("Inserting embeddings into vector database...")

        # Insert all embeddings into the database
        insertion_start = time.time()
        for text, embedding in zip(list_of_text, embeddings):
            # Convert to numpy array and store
            self.insert(text, np.array(embedding))

        # Calculate and log final statistics
        total_time = time.time() - start_time
        insertion_time = time.time() - insertion_start

        if self.enable_logging:
            self.logger.info(f"Vector database built successfully in {total_time:.2f}s")
            self.logger.info(
                f"  - Embedding creation: {total_time - insertion_time:.2f}s"
            )
            self.logger.info(f"  - Database insertion: {insertion_time:.3f}s")
            self.logger.info(f"Total vectors stored: {len(self.vectors)}")

            # Log memory/storage insights
            if embeddings:
                embedding_dim = len(embeddings[0])
                total_values = len(self.vectors) * embedding_dim

                # Calculate theoretical memory usage (just the data)
                bytes_per_float = 8  # float64
                theoretical_bytes = total_values * bytes_per_float
                theoretical_mb = theoretical_bytes / (1024 * 1024)

                # Calculate actual memory usage (including Python overhead)
                import sys

                actual_memory = sys.getsizeof(self.vectors)
                for key, vector in self.vectors.items():
                    actual_memory += sys.getsizeof(key) + sys.getsizeof(vector)
                actual_mb = actual_memory / (1024 * 1024)

                # Calculate overhead percentage
                overhead_percent = (
                    (actual_memory - theoretical_bytes) / theoretical_bytes
                ) * 100

                self.logger.info(f"Vector dimensions: {embedding_dim}")
                self.logger.info(
                    f"Storage size: {len(self.vectors)} × {embedding_dim} = {total_values:,} values"
                )
                self.logger.info(
                    f"Theoretical memory: {theoretical_bytes:,} bytes ({theoretical_mb:.2f} MB)"
                )
                self.logger.info(
                    f"Actual memory: {actual_memory:,} bytes ({actual_mb:.2f} MB)"
                )
                self.logger.info(f"Memory overhead: {overhead_percent:.1f}%")

        return self


if __name__ == "__main__":
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    k = 2

    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k)
    print(f"Closest {k} vector(s):", searched_vector)

    retrieved_vector = vector_db.retrieve_from_key(
        "I like to eat broccoli and bananas."
    )
    print("Retrieved vector:", retrieved_vector)

    relevant_texts = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, return_as_text=True
    )
    print(f"Closest {k} text(s):", relevant_texts)
