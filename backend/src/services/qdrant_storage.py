from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from ..models.embedding_vector import EmbeddingVector
from ..models.metadata import Metadata
from ..lib.utils import get_qdrant_client, create_embeddings_collection
from ..lib.logging import logger
from uuid import uuid4

class QdrantStorageService:
    """
    Service for storing embeddings in Qdrant vector database with metadata linking back to source documents.
    """

    def __init__(self, collection_name: str = "rag_embeddings"):
        """
        Initialize the Qdrant storage service.

        Args:
            collection_name: Name of the Qdrant collection to use
        """
        self.client = get_qdrant_client()
        self.collection_name = collection_name

        # Create collection if it doesn't exist
        create_embeddings_collection(self.client, self.collection_name)

    def save_embeddings(self, embedding_vectors: List[EmbeddingVector], metadata_list: List[Metadata]) -> bool:
        """
        Save a list of embedding vectors to Qdrant with their metadata.

        Args:
            embedding_vectors: List of EmbeddingVector objects to save
            metadata_list: List of corresponding Metadata objects

        Returns:
            bool: True if embeddings were saved successfully
        """
        if len(embedding_vectors) != len(metadata_list):
            raise ValueError("Number of embeddings must match number of metadata objects")

        try:
            points = []
            for embedding_vector, metadata in zip(embedding_vectors, metadata_list):
                point = models.PointStruct(
                    id=embedding_vector.id,
                    vector=embedding_vector.vector,
                    payload=metadata.to_payload()
                )
                points.append(point)

            # Upload points to Qdrant
            self.client.upload_points(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully saved {len(embedding_vectors)} embeddings to collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Error saving embeddings to Qdrant: {str(e)}")
            raise

    def save_embedding(self, embedding_vector: EmbeddingVector, metadata: Metadata) -> bool:
        """
        Save a single embedding vector to Qdrant with its metadata.

        Args:
            embedding_vector: EmbeddingVector object to save
            metadata: Corresponding Metadata object

        Returns:
            bool: True if embedding was saved successfully
        """
        try:
            point = models.PointStruct(
                id=embedding_vector.id,
                vector=embedding_vector.vector,
                payload=metadata.to_payload()
            )

            # Upload point to Qdrant
            self.client.upload_points(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Successfully saved embedding {embedding_vector.id} to collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Error saving embedding to Qdrant: {str(e)}")
            raise

    def retrieve_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve similar embeddings from Qdrant based on a query vector.

        Args:
            query_vector: Vector to search for similar embeddings
            top_k: Number of similar embeddings to retrieve

        Returns:
            List[Dict[str, Any]]: List of similar embeddings with metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                    "vector": result.vector
                }
                formatted_results.append(formatted_result)

            logger.info(f"Retrieved {len(formatted_results)} similar embeddings")
            return formatted_results

        except Exception as e:
            logger.error(f"Error retrieving similar embeddings from Qdrant: {str(e)}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the Qdrant collection.

        Returns:
            Dict[str, Any]: Collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.point_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            raise

    def validate_metadata_linkage(self, embedding_ids: List[str], expected_source_files: List[str]) -> bool:
        """
        Validate that embeddings have proper metadata linkage to source files.

        Args:
            embedding_ids: List of embedding IDs to validate
            expected_source_files: List of expected source files

        Returns:
            bool: True if metadata linkage is valid
        """
        try:
            # Fetch points from Qdrant
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=embedding_ids
            )

            # Check if all records have proper source file metadata
            for record in records:
                payload = record.payload
                if not payload or not payload.get('source_file'):
                    logger.warning(f"Embedding {record.id} missing source file metadata")
                    return False

            logger.info(f"Validated metadata linkage for {len(embedding_ids)} embeddings")
            return True

        except Exception as e:
            logger.error(f"Error validating metadata linkage: {str(e)}")
            return False

    def delete_collection(self) -> bool:
        """
        Delete the Qdrant collection.

        Returns:
            bool: True if collection was deleted successfully
        """
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise

    def create_new_collection(self, collection_name: str, vector_size: int = 768) -> bool:
        """
        Create a new Qdrant collection with the specified name and vector size.

        Args:
            collection_name: Name of the collection to create
            vector_size: Size of the embedding vectors

        Returns:
            bool: True if collection was created successfully
        """
        try:
            create_embeddings_collection(self.client, collection_name, vector_size)
            self.collection_name = collection_name
            logger.info(f"Created new collection '{collection_name}'")
            return True
        except Exception as e:
            logger.error(f"Error creating new collection: {str(e)}")
            raise