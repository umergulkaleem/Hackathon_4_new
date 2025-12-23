---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Code
command: /sp.constitution
labels: [constitution,specification,ai-book,rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: AI-Spec-Driven Book with Embedded RAG Chatbot

Objective:
Author and deploy a technical book using Spec-Kit Plus and Claude Code, published via Docusaurus on GitHub Pages, with an embedded RAG chatbot answering questions strictly from the book content.

Core Principles:
- Specification-first, AI-native development
- Accuracy via authoritative sources only
- Clarity for CS/software engineering audience
- Reproducibility of build, deploy, and AI systems
- Zero hallucination tolerance

Book Standards:
- Framework: Docusaurus
- Authorship: Spec-Kit Plus + Claude Code
- Writing level: Flesch-Kincaid 10–12
- Consistent terminology and runnable code examples

Deployment:
- GitHub Pages hosting
- Versioned specs, content, and build instructions

RAG Chatbot:
- Scope-limited to book content only
- Supports full-book and user-selected text Q&A
- Stack: OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant Cloud
- Must cite source section or state "answer not found"

Security & Data:
- Environment-based secrets only
- Minimal data retention

Quality Gates:
- Spec-content-chatbot alignment
- No plagiarism
- No undocumented APIs

Success Criteria:
- Live book on GitHub Pages
- Functional embedded RAG chatbot
- Accurate, source-grounded responses

## Response snapshot

Created a comprehensive constitution file for the AI-Spec-Driven Book with Embedded RAG Chatbot project. The constitution includes 6 core principles:

1. Specification-First, AI-Native Development
2. Accuracy via Authoritative Sources Only
3. Clarity for CS/Software Engineering Audience
4. Reproducibility of Build, Deploy, and AI Systems
5. Zero Hallucination Tolerance
6. Docusaurus-Based Publication Framework

Additional sections cover deployment requirements, RAG chatbot specifications, quality gates, authoring process, testing requirements, and review processes. The constitution establishes governance guidelines and version tracking.

## Outcome

- ✅ Impact: Created project constitution that establishes clear principles and guidelines for the AI-Spec-Driven Book with Embedded RAG Chatbot project
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Continue with specification, planning, and implementation phases
- 🧠 Reflection: Constitution provides solid foundation for maintaining quality and consistency throughout the project lifecycle

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin specification phase with /sp.specify