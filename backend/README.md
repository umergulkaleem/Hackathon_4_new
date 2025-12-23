# Markdown to Vector Embeddings Service

This service transforms Docusaurus-generated Markdown content into vector embeddings for RAG (Retrieval-Augmented Generation) chatbot applications.

## Overview

The system processes Markdown files, extracts clean text, performs semantic chunking, generates embeddings using Cohere API, and stores them in Qdrant with proper metadata linkage. This enables accurate, context-aware retrieval for RAG systems.

## Features

- Extract clean text from Markdown files while preserving document structure
- Semantic chunking that respects document hierarchy
- Embedding generation using Cohere API
- Storage in Qdrant vector database with metadata
- Quality validation and assurance
- Document hierarchy preservation

## Prerequisites

- Python 3.11+
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Usage

Run the main processing pipeline:

```bash
python src/api/main.py
```

The system will:
1. Get all URLs from the deployed site
2. Extract text from the URLs
3. Chunk the text semantically
4. Generate embeddings using Cohere
5. Create Qdrant collection named "rag_embeddings"
6. Save embeddings with metadata to Qdrant

## Architecture

- `src/models/` - Data models for Markdown content, text chunks, embeddings, and metadata
- `src/services/` - Business logic for text extraction, chunking, embedding, and storage
- `src/api/` - Main application entry point
- `src/lib/` - Configuration, logging, and utility functions

## Environment Variables

- `COHERE_API_KEY` - Your Cohere API key (required)
- `QDRANT_URL` - URL for Qdrant instance (default: http://localhost:6333)
- `QDRANT_API_KEY` - API key for Qdrant (if required)
- `DEFAULT_CHUNK_SIZE` - Size of text chunks (default: 1000)
- `DEFAULT_CHUNK_OVERLAP` - Overlap between chunks (default: 200)
- `DEFAULT_EMBEDDING_MODEL` - Cohere model to use (default: embed-multilingual-v2.0)

## Services

- `TextExtractionService` - Extracts clean text from Markdown files/URLs
- `SemanticChunkingService` - Chunks text while preserving document structure
- `EmbeddingGeneratorService` - Generates embeddings using Cohere API
- `QdrantStorageService` - Stores embeddings in Qdrant with metadata
- `EmbeddingValidatorService` - Validates embedding quality and metadata linkage

## Configuration

The system can be configured via environment variables in the `.env` file. Default values are provided for all configuration options.