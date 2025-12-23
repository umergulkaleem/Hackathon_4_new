# Quickstart: Markdown to Vector Embeddings for RAG Chatbot

## Prerequisites
- Python 3.11+
- pip package manager
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-name>/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file with the following:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here  # For example: https://your-cluster.qdrant.tech:6333
QDRANT_API_KEY=your_qdrant_api_key_here  # If using cloud instance
```

## Usage

### 1. Run the Processing Pipeline
```bash
cd backend
python src/api/main.py
```

### 2. Process Specific Markdown Directory
```bash
# The main.py file can be modified to process specific directories
# By default, it processes content from the deployed site
```

### 3. Process Single File (Custom Implementation)
To process a single file, you can create a custom script using the services:

```python
from src.services.text_extraction import TextExtractionService
from src.services.semantic_chunking import SemanticChunkingService
from src.services.embedding_generator import EmbeddingGeneratorService
from src.services.qdrant_storage import QdrantStorageService

# Initialize services
text_service = TextExtractionService()
chunking_service = SemanticChunkingService()
embedding_service = EmbeddingGeneratorService()
storage_service = QdrantStorageService()

# Extract content
content = text_service.extract_from_file('/path/to/your/file.md')

# Chunk content
chunks = chunking_service.chunk_markdown_content(content)

# Generate embeddings
embeddings = embedding_service.batch_generate_embeddings(chunks)

# Create metadata and save to Qdrant
# (Implementation details as per main.py)
```

## API Endpoints (when running as service)
- `POST /process` - Process Markdown content and generate embeddings
- `GET /status` - Check processing status

## Configuration Options
- `DEFAULT_CHUNK_SIZE`: Maximum characters per text chunk (default: 1000)
- `DEFAULT_CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `DEFAULT_EMBEDDING_MODEL`: Embedding model to use (default: embed-multilingual-v2.0)

## Local Qdrant Setup
If running locally:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

The service will automatically create the "rag_embeddings" collection if it doesn't exist.

## Validation
After running the pipeline, verify:
1. Embeddings are stored in Qdrant collection "rag_embeddings"
2. Metadata includes proper source file references
3. Document hierarchy is preserved in chunking
4. Quality validation passed (90%+ quality score)