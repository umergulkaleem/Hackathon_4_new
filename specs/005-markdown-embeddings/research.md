# Research: Markdown to Vector Embeddings for RAG Chatbot

## Decision: Technology Stack Selection
**Rationale**: Using Python with Cohere for embeddings and Qdrant for vector storage based on user requirements and industry standards for RAG systems.
**Alternatives considered**:
- OpenAI embeddings vs Cohere: Cohere was specified in user requirements
- Pinecone vs Qdrant vs Weaviate: Qdrant was specified in user requirements
- Node.js vs Python: Python has better ecosystem for text processing and ML

## Decision: Text Extraction from Markdown
**Rationale**: Using BeautifulSoup4 and markdown libraries to extract clean text from Docusaurus-generated Markdown, preserving document structure.
**Alternatives considered**:
- Direct regex parsing: Less reliable for complex Markdown
- Pandoc: Additional dependency complexity
- markdown2 + BeautifulSoup4: Best balance of simplicity and reliability

## Decision: Semantic Chunking Strategy
**Rationale**: Using recursive character text splitter that respects document hierarchy (headers, sections) to maintain context.
**Alternatives considered**:
- Fixed-size token chunks: May split contextually related content
- Sentence-based chunks: May not respect document structure
- Recursive character splitting: Maintains context while allowing for semantic boundaries

## Decision: Qdrant Collection Structure
**Rationale**: Creating a "rag_embeddings" collection with metadata fields for source tracking and content hierarchy.
**Alternatives considered**:
- Multiple collections by document type: More complex querying
- Single collection with metadata: Simpler management and retrieval

## Decision: Embedding Dimension and Model
**Rationale**: Using Cohere's recommended embedding model (e.g., embed-multilingual-v2.0) with appropriate dimensionality.
**Alternatives considered**:
- Different Cohere models: Multilingual model handles diverse content well
- Custom embedding models: Cohere provides good balance of quality and cost