# Data Model: Markdown to Vector Embeddings for RAG Chatbot

## Entities

### MarkdownContent
- **id**: string (unique identifier for the source document)
- **file_path**: string (path to the original Markdown file)
- **content**: string (raw Markdown content)
- **title**: string (document title extracted from Markdown)
- **headers**: list (document structure: headings and their hierarchy)
- **created_at**: datetime (timestamp when content was processed)
- **updated_at**: datetime (timestamp when content was last updated)

### TextChunk
- **id**: string (unique identifier for the chunk)
- **content**: string (clean text content of the chunk)
- **chunk_index**: integer (position of the chunk in the original document)
- **source_document_id**: string (reference to MarkdownContent.id)
- **headers_context**: list (headers that provide context for this chunk)
- **word_count**: integer (number of words in the chunk)
- **char_count**: integer (number of characters in the chunk)

### EmbeddingVector
- **id**: string (unique identifier for the embedding)
- **vector**: list[float] (the actual embedding vector values)
- **chunk_id**: string (reference to TextChunk.id)
- **model**: string (name of the embedding model used)
- **created_at**: datetime (timestamp when embedding was generated)
- **dimension**: integer (dimensionality of the embedding vector)

### Metadata
- **source_file**: string (original file path)
- **document_title**: string (title of the source document)
- **chunk_index**: integer (position in the original document)
- **headers_hierarchy**: string (flattened representation of document headers)
- **word_count**: integer (number of words in the chunk)
- **content_type**: string (type of content: text, code, list, etc.)
- **retrieval_score**: float (score from similarity search, if applicable)

## Relationships
- MarkdownContent (1) → TextChunk (many): One document can be chunked into many text chunks
- TextChunk (1) → EmbeddingVector (1): Each text chunk has one corresponding embedding vector
- EmbeddingVector (many) → Metadata (1): Each embedding has associated metadata

## Validation Rules
- MarkdownContent.file_path must be a valid path
- TextChunk.word_count must be > 0 and < 10000 (reasonable chunk size)
- EmbeddingVector.vector must have consistent dimensionality
- Metadata.source_file must reference an existing MarkdownContent

## State Transitions
- MarkdownContent: DRAFT → PROCESSING → EMBEDDED → INDEXED
- TextChunk: CREATED → CHUNKED → EMBEDDED → STORED
- EmbeddingVector: REQUESTED → GENERATED → STORED → RETRIEVABLE