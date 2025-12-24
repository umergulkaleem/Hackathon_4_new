# Quickstart: RAG Retrieval Validation

## Prerequisites

- Python 3.11 or higher
- Access to Qdrant vector database with existing embeddings from Spec-1
- Cohere API key for query vectorization
- (Optional) Local Qdrant instance or Qdrant Cloud access

## Setup

### 1. Install Dependencies

```bash
pip install qdrant-client cohere python-dotenv
```

### 2. Configure Environment

Create a `.env` file in the project root with the following variables:

```env
QDRANT_HOST=your-qdrant-host
QDRANT_PORT=6333  # Default for local, omit for cloud
QDRANT_API_KEY=your-api-key  # Required for cloud instances
COHERE_API_KEY=your-cohere-api-key
QDRANT_COLLECTION_NAME=your-collection-name  # From Spec-1
COHERE_MODEL=embed-multilingual-v2.0  # Or the model used in Spec-1
```

### 3. Identify Collection Parameters

From Spec-1, you'll need to know:
- Collection name where vectors are stored
- Vector dimension size
- Cohere model used for embeddings

## Usage

### Basic Validation

```bash
python retrieve.py --query "What is the main concept of vector embeddings?"
```

### Advanced Options

```bash
# Specify top-k results (default: 5)
python retrieve.py --query "Explain RAG systems" --top-k 10

# Specify minimum similarity score (default: 0.0)
python retrieve.py --query "How does retrieval work?" --min-score 0.5

# Run multiple test queries from a file
python retrieve.py --query-file test_queries.txt

# Run comprehensive validation with detailed output
python retrieve.py --query "Your query here" --verbose
```

### Input Validation

The script includes comprehensive input validation:
- `--top-k` must be a positive integer
- `--min-score` must be between 0.0 and 1.0
- Either `--query` or `--query-file` must be provided (but not both)
- Query file must exist and be readable

## Validation Process

The script performs these validation steps:

1. **Connection Test**: Verifies connection to Qdrant database
2. **Collection Check**: Confirms the expected collection exists
3. **Vector Schema Validation**: Ensures vector dimensions match
4. **Query Test**: Performs similarity search with provided query
5. **Content Validation**: Verifies retrieved content matches source URLs and metadata
6. **Result Accuracy**: Validates that results are relevant to the query

## Expected Output

```text
Validation Results:
- Connection: ✅ Connected to Qdrant successfully
- Collection: ✅ Found 'book_content_vectors' collection
- Query: "What are vector embeddings?"
- Results: 5 relevant chunks retrieved
- Content Validation: ✅ All source URLs and metadata match
- Performance: Query completed in 1.2s
- Overall: ✅ Validation passed
```

## Troubleshooting

### Common Issues

**Connection Error**:
- Check QDRANT_HOST and QDRANT_API_KEY in .env
- Verify Qdrant service is running

**Collection Not Found**:
- Confirm QDRANT_COLLECTION_NAME matches Spec-1
- Verify vectors were created in previous step

**Dimension Mismatch**:
- Ensure Cohere model matches the one used in Spec-1
- Check that query embeddings match stored vector dimensions

### Validation Failures

If validation fails, the script will provide specific error messages:
- Connection issues: "Failed to connect to Qdrant: [details]"
- Content mismatch: "Retrieved content doesn't match source URL: [details]"
- Performance issues: "Query took longer than expected: [time]s"