# Data Model: RAG Retrieval Validation

## Entities

### QdrantVectorRecord
**Description**: Represents a single vector record stored in Qdrant with associated metadata

**Fields**:
- `id` (str): Unique identifier for the vector record
- `vector` (list[float]): The embedding vector representation of text content
- `payload` (dict):
  - `content` (str): Original text content that was embedded
  - `source_url` (str): URL or identifier of the source document
  - `metadata` (dict): Additional metadata associated with the content
    - `title` (str): Title of the source document
    - `section` (str): Section or chapter of the source
    - `created_at` (str): Timestamp when the vector was created
    - `chunk_id` (str): Identifier for this specific text chunk

### QueryRequest
**Description**: Represents a validation query request

**Fields**:
- `query_text` (str): The text to be converted to an embedding for similarity search
- `top_k` (int): Number of similar results to retrieve (default: 5)
- `min_score` (float): Minimum similarity score threshold (default: 0.0)

### QueryResult
**Description**: Represents the results of a similarity search query

**Fields**:
- `id` (str): Unique identifier of the matched vector record
- `score` (float): Similarity score between query and result
- `content` (str): Text content of the matched record
- `source_url` (str): Source URL of the matched record
- `metadata` (dict): Metadata associated with the matched record
- `vector_distance` (float): Distance measure used in similarity calculation

### ValidationResult
**Description**: Represents the validation result for a query and its results

**Fields**:
- `query` (str): Original query text
- `results` (list[QueryResult]): List of top-k results returned
- `validation_passed` (bool): Whether all validation checks passed
- `validation_details` (list[dict]):
  - `check_type` (str): Type of validation performed
  - `passed` (bool): Whether this specific check passed
  - `message` (str): Details about the validation result
- `execution_time` (float): Time taken to execute the query in seconds

## Relationships

- `QueryRequest` → `QueryResult` (one-to-many): A single query produces multiple results
- `QueryResult` → `ValidationResult` (many-to-one): Multiple results are validated together
- `QdrantVectorRecord` → `QueryResult` (one-to-many): One stored record can match multiple queries

## Validation Rules

### From Functional Requirements
- **FR-001**: Connection validation - Must successfully connect to Qdrant
- **FR-002**: Query validation - Must return top-k relevant text chunks
- **FR-003**: Content validation - Retrieved content must match source URLs and metadata
- **FR-007**: Error message validation - Must provide clear error messages when validation fails

### Data Integrity Rules
- Source URL format must be valid
- Content field must not be empty
- Vector dimensions must match expected size
- Metadata must contain required fields (source_url, content)

## State Transitions

### Query Process Flow
1. `QueryRequest` (created) → (validated) → (vectorized) → (searched)
2. `QueryResult` (retrieved) → (validated) → (aggregated)
3. `ValidationResult` (computed) → (reported)