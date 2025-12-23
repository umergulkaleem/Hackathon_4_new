from typing import List, Dict, Any, Tuple
from ..models.embedding_vector import EmbeddingVector
from ..models.metadata import Metadata
from ..lib.logging import logger
import numpy as np
from scipy.spatial.distance import cosine
from collections import Counter

class EmbeddingValidatorService:
    """
    Service for validating that generated embeddings accurately represent the source content.
    """

    def __init__(self):
        """
        Initialize the embedding validation service.
        """
        pass

    def validate_embeddings_quality(self, embeddings: List[EmbeddingVector]) -> Dict[str, Any]:
        """
        Validate the quality of generated embeddings.

        Args:
            embeddings: List of EmbeddingVector to validate

        Returns:
            Dict[str, Any]: Validation results and quality metrics
        """
        if not embeddings:
            return {
                "valid": False,
                "message": "No embeddings provided",
                "metrics": {}
            }

        # Check embedding dimensions consistency
        dimensions = [len(embed.vector) for embed in embeddings]
        dimension_consistency = len(set(dimensions)) == 1

        # Calculate quality metrics
        avg_dimension = sum(dimensions) / len(dimensions) if dimensions else 0
        min_dimension = min(dimensions) if dimensions else 0
        max_dimension = max(dimensions) if dimensions else 0

        # Check for zero vectors (indicating potential issues)
        zero_vectors = 0
        for embed in embeddings:
            if all(v == 0.0 for v in embed.vector):
                zero_vectors += 1

        # Calculate embedding diversity (simple approach using cosine similarity)
        diversity_score = self._calculate_diversity_score(embeddings)

        validation_result = {
            "valid": dimension_consistency and zero_vectors == 0,
            "message": "Embeddings validated successfully" if dimension_consistency and zero_vectors == 0 else "Embeddings have issues",
            "metrics": {
                "total_embeddings": len(embeddings),
                "dimension_consistency": dimension_consistency,
                "avg_dimension": avg_dimension,
                "min_dimension": min_dimension,
                "max_dimension": max_dimension,
                "zero_vectors_count": zero_vectors,
                "diversity_score": diversity_score,
                "quality_percentage": (len(embeddings) - zero_vectors) / len(embeddings) * 100 if embeddings else 0
            }
        }

        logger.info(f"Embedding validation completed: {validation_result['message']}")
        return validation_result

    def validate_metadata_linkage(self, embeddings: List[EmbeddingVector], metadata_list: List[Metadata]) -> Dict[str, Any]:
        """
        Validate that embeddings have proper metadata linkage.

        Args:
            embeddings: List of EmbeddingVector to validate
            metadata_list: List of corresponding Metadata objects

        Returns:
            Dict[str, Any]: Validation results for metadata linkage
        """
        if len(embeddings) != len(metadata_list):
            return {
                "valid": False,
                "message": f"Mismatch between embeddings ({len(embeddings)}) and metadata ({len(metadata_list)}) count",
                "metrics": {
                    "embedding_count": len(embeddings),
                    "metadata_count": len(metadata_list)
                }
            }

        # Check for proper linkage
        missing_links = 0
        for i, embed in enumerate(embeddings):
            meta = metadata_list[i]
            if not meta.source_file or meta.source_file == "unknown":
                missing_links += 1

        linkage_valid = missing_links == 0

        validation_result = {
            "valid": linkage_valid,
            "message": "Metadata linkage validated successfully" if linkage_valid else "Some embeddings lack proper metadata linkage",
            "metrics": {
                "total_items": len(embeddings),
                "missing_links": missing_links,
                "linkage_percentage": ((len(embeddings) - missing_links) / len(embeddings) * 100) if embeddings else 0
            }
        }

        logger.info(f"Metadata linkage validation completed: {validation_result['message']}")
        return validation_result

    def calculate_quality_metrics(self, embeddings: List[EmbeddingVector], metadata_list: List[Metadata] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive quality metrics for embeddings.

        Args:
            embeddings: List of EmbeddingVector to analyze
            metadata_list: Optional list of corresponding Metadata objects

        Returns:
            Dict[str, Any]: Comprehensive quality metrics
        """
        if not embeddings:
            return {"error": "No embeddings provided"}

        # Basic metrics
        metrics = {
            "total_embeddings": len(embeddings),
            "dimension_analysis": self._analyze_dimensions(embeddings),
            "similarity_analysis": self._analyze_similarity(embeddings),
            "embedding_distribution": self._analyze_distribution(embeddings)
        }

        # If metadata is provided, include metadata-specific metrics
        if metadata_list:
            metrics["metadata_analysis"] = self._analyze_metadata(metadata_list)

        return metrics

    def _calculate_diversity_score(self, embeddings: List[EmbeddingVector]) -> float:
        """
        Calculate a simple diversity score based on cosine similarity between embeddings.

        Args:
            embeddings: List of EmbeddingVector

        Returns:
            float: Diversity score (0-1, where 1 is most diverse)
        """
        if len(embeddings) < 2:
            return 1.0  # Perfectly diverse if only one embedding

        # Sample a subset for performance (if too many embeddings)
        sample_size = min(20, len(embeddings))
        sample_embeddings = embeddings[:sample_size]

        similarities = []
        for i in range(len(sample_embeddings)):
            for j in range(i + 1, len(sample_embeddings)):
                sim = 1 - cosine(sample_embeddings[i].vector, sample_embeddings[j].vector)
                similarities.append(sim)

        if not similarities:
            return 1.0

        # Average similarity (lower = more diverse)
        avg_similarity = sum(similarities) / len(similarities)
        # Convert to diversity score (1 - similarity)
        diversity_score = 1 - avg_similarity
        return max(0.0, diversity_score)  # Ensure non-negative

    def _analyze_dimensions(self, embeddings: List[EmbeddingVector]) -> Dict[str, Any]:
        """
        Analyze embedding dimensions.

        Args:
            embeddings: List of EmbeddingVector

        Returns:
            Dict[str, Any]: Dimension analysis results
        """
        if not embeddings:
            return {}

        dimensions = [len(embed.vector) for embed in embeddings]
        return {
            "min": min(dimensions),
            "max": max(dimensions),
            "avg": sum(dimensions) / len(dimensions),
            "std_dev": np.std(dimensions) if len(dimensions) > 1 else 0,
            "consistent": len(set(dimensions)) == 1
        }

    def _analyze_similarity(self, embeddings: List[EmbeddingVector]) -> Dict[str, Any]:
        """
        Analyze similarity between embeddings.

        Args:
            embeddings: List of EmbeddingVector

        Returns:
            Dict[str, Any]: Similarity analysis results
        """
        if len(embeddings) < 2:
            return {"message": "Need at least 2 embeddings for similarity analysis"}

        # Calculate similarity metrics
        similarities = []
        for i in range(min(10, len(embeddings))):  # Sample first 10 for performance
            for j in range(i + 1, min(10, len(embeddings))):
                sim = 1 - cosine(embeddings[i].vector, embeddings[j].vector)
                similarities.append(sim)

        if not similarities:
            return {}

        return {
            "min_similarity": min(similarities),
            "max_similarity": max(similarities),
            "avg_similarity": sum(similarities) / len(similarities),
            "std_dev": np.std(similarities) if len(similarities) > 1 else 0
        }

    def _analyze_distribution(self, embeddings: List[EmbeddingVector]) -> Dict[str, Any]:
        """
        Analyze the distribution of embedding values.

        Args:
            embeddings: List of EmbeddingVector

        Returns:
            Dict[str, Any]: Distribution analysis results
        """
        if not embeddings:
            return {}

        # Sample first embedding to get dimension count
        sample_embedding = embeddings[0].vector
        values = []
        for embed in embeddings[:10]:  # Sample first 10 for performance
            values.extend(embed.vector)

        if not values:
            return {}

        return {
            "min_value": min(values),
            "max_value": max(values),
            "avg_value": sum(values) / len(values),
            "std_dev": np.std(values),
            "zero_count": values.count(0.0)
        }

    def _analyze_metadata(self, metadata_list: List[Metadata]) -> Dict[str, Any]:
        """
        Analyze metadata quality and distribution.

        Args:
            metadata_list: List of Metadata objects

        Returns:
            Dict[str, Any]: Metadata analysis results
        """
        if not metadata_list:
            return {}

        # Count missing values
        missing_source_files = sum(1 for meta in metadata_list if not meta.source_file or meta.source_file == "unknown")
        missing_titles = sum(1 for meta in metadata_list if not meta.document_title or meta.document_title == "unknown")

        # Content type distribution
        content_types = [meta.content_type for meta in metadata_list]
        type_distribution = dict(Counter(content_types))

        return {
            "total_metadata": len(metadata_list),
            "missing_source_files": missing_source_files,
            "missing_titles": missing_titles,
            "content_type_distribution": type_distribution,
            "source_file_diversity": len(set(meta.source_file for meta in metadata_list if meta.source_file != "unknown"))
        }

    def generate_quality_report(self, embeddings: List[EmbeddingVector], metadata_list: List[Metadata] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive quality report for embeddings and metadata.

        Args:
            embeddings: List of EmbeddingVector to report on
            metadata_list: Optional list of corresponding Metadata objects

        Returns:
            Dict[str, Any]: Comprehensive quality report
        """
        report = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "embedding_validation": self.validate_embeddings_quality(embeddings),
            "metadata_validation": self.validate_metadata_linkage(embeddings, metadata_list) if metadata_list else None,
            "quality_metrics": self.calculate_quality_metrics(embeddings, metadata_list)
        }

        # Determine overall quality score
        embed_valid = report["embedding_validation"]["valid"]
        metadata_valid = report["metadata_validation"]["valid"] if metadata_valid else True

        report["overall_quality_score"] = (
            (report["embedding_validation"]["metrics"]["quality_percentage"] +
             report["metadata_validation"]["metrics"]["linkage_percentage"] if metadata_valid else 100) / 2
        ) if embed_valid else 0

        return report