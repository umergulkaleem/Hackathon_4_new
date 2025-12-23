<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.0.0
Modified principles: None (new constitution)
Added sections: All principles and sections
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# AI-Spec-Driven Book with Embedded RAG Chatbot Constitution

## Core Principles

### Specification-First, AI-Native Development
All development begins with clear, detailed specifications that guide implementation. AI tools (Claude Code, Spec-Kit Plus) are integral to the development process, not supplementary. Specifications must be precise enough to enable automated implementation and testing.

### Accuracy via Authoritative Sources Only
No assumptions or internal knowledge without external verification. All information, APIs, and implementation details must come from authoritative sources. Code must reference specific files/lines. Zero tolerance for hallucinations or fabricated information.

### Clarity for CS/Software Engineering Audience
Content and code must be accessible to computer science and software engineering professionals. Writing level should be Flesch-Kincaid grade 10-12. Technical concepts must be explained with runnable code examples and consistent terminology.

### Reproducibility of Build, Deploy, and AI Systems
All processes must be reproducible. Build instructions, deployment procedures, and AI system configurations must be version-controlled and documented. Anyone should be able to reproduce the complete system from scratch using provided instructions.

### Zero Hallucination Tolerance
The RAG chatbot must strictly answer questions only from book content. If information is not found, it must state "answer not found" rather than generating plausible-sounding but incorrect responses. This applies to both the AI system and the development process.

### Docusaurus-Based Publication Framework
Technical book content must be authored using Docusaurus framework for consistent presentation, navigation, and deployment to GitHub Pages. Content structure must follow Docusaurus conventions and be versioned appropriately.

## Additional Constraints

### Deployment Requirements
- GitHub Pages hosting with versioned content
- Automated build and deployment pipeline
- Maintained build instructions for all environments

### RAG Chatbot Specifications
- Scope limited to book content only
- Supports full-book and user-selected text Q&A
- Technology stack: OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant Cloud
- Must cite source sections or explicitly state "answer not found"
- Environment-based secrets only, minimal data retention

### Quality Gates
- Spec-content-chatbot alignment verification
- No plagiarism detection
- No undocumented APIs or features
- All code examples must be tested and runnable

## Development Workflow

### Authoring Process
- Use Spec-Kit Plus and Claude Code for specification-first development
- All changes must be tracked with precise file/line references
- Smallest viable diffs preferred
- No unrelated refactoring during feature implementation

### Testing Requirements
- All code examples must be runnable and tested
- Chatbot accuracy must be validated against source content
- Build/deployment process must be tested in clean environment
- Cross-platform compatibility verification

### Review Process
- Specification completeness check
- Technical accuracy verification
- Code example validation
- Chatbot response accuracy testing

## Governance

This constitution governs all aspects of the AI-Spec-Driven Book with Embedded RAG Chatbot project. All development activities, code changes, and feature implementations must comply with these principles. Amendments to this constitution require explicit documentation of changes, impact assessment, and team approval. All pull requests and reviews must verify compliance with constitutional principles. Version control and documentation of all changes is mandatory.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
