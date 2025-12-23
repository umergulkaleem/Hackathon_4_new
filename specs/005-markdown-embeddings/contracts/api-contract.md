# API Contract: Markdown to Embeddings Service

## Process Markdown Endpoint
- **Endpoint**: `POST /process`
- **Description**: Process Markdown content and generate vector embeddings
- **Request Body**:
  ```json
  {
    "input_path": "/path/to/markdown/files",
    "collection_name": "rag_embeddings",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "model": "embed-multilingual-v2.0"
  }
  ```
- **Response**:
  ```json
  {
    "status": "processing|completed|error",
    "processed_files": 10,
    "generated_embeddings": 150,
    "collection_name": "rag_embeddings",
    "processing_time": "2.5s"
  }
  ```

## Status Check Endpoint
- **Endpoint**: `GET /status`
- **Description**: Check the processing status of the service
- **Response**:
  ```json
  {
    "status": "ready|processing|error",
    "active_processes": 0,
    "total_embeddings": 1500,
    "collections": ["rag_embeddings"],
    "last_processed": "2025-12-23T10:30:00Z"
  }
  ```

## Individual File Processing
- **Endpoint**: `POST /process-file`
- **Description**: Process a single Markdown file and generate embeddings
- **Request Body**:
  ```json
  {
    "file_path": "/path/to/file.md",
    "collection_name": "rag_embeddings",
    "chunk_size": 1000
  }
  ```
- **Response**:
  ```json
  {
    "status": "completed",
    "file_path": "/path/to/file.md",
    "chunks_created": 5,
    "embeddings_generated": 5,
    "collection_name": "rag_embeddings"
  }
  ```