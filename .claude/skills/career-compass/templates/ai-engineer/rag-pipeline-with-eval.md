---
title: "RAG Pipeline with Evaluation Harness"
track: "ai-engineer"
difficulty_tier: "intermediate"
estimated_hours: 20
role: "core"
skill_tags: ["retrieval-augmented-generation", "vector-databases", "embeddings", "eval-harnesses", "prompt-engineering", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# RAG Pipeline with Evaluation Harness

## Production Workflow Mirrored
1. Document ingestion & preprocessing
2. Chunking strategy
3. Embedding & indexing into a vector store
4. Retrieval (top-k, reranking)
5. Generation (prompt construction, LLM call)
6. Evaluation harness (retrieval precision/recall, answer faithfulness)
7. Basic deploy (simple API endpoint) & lightweight monitoring (latency, failure logging)

## What You'll Build
A question-answering system over a document set of your choice that retrieves
relevant chunks and generates grounded answers, with a small evaluation suite that
scores the system on a hand-built question set so you can quantify quality, not just
eyeball it.

## Student-Scope Notes
- Local/open-source vector store (Chroma, FAISS) instead of a managed production
  service — same retrieval concepts, no infra cost or ops overhead.
- Eval set is ~20-30 hand-labeled Q&A pairs, not a large annotated benchmark.
- "Deploy" means a local FastAPI/Flask endpoint hit with curl, not a scaled cloud
  deployment — the API-boundary and monitoring concepts are the point, not infra
  (that's a separate template).

## Steps
1. Pick a document set (10-50 documents) relevant to a domain you care about.
2. Build ingestion + chunking (try 2 strategies, compare).
3. Embed chunks and index into a vector store.
4. Build retrieval (plain top-k, then add reranking).
5. Build generation: grounded prompt from retrieved chunks, call an LLM.
6. Hand-write 20-30 Q&A pairs with expected answers/source chunks.
7. Build an eval script scoring retrieval hit-rate and answer faithfulness.
8. Wrap in a minimal API endpoint; log latency and failures to a file.
9. Write up: chunking/retrieval choices and why, eval results, what you'd change for scale.

## Extension Ideas
- Add hybrid search (keyword + vector).
- Add a feedback loop flagging low-confidence answers for human review.
- Swap the local vector store for a managed one and note the tradeoffs.
- Add basic cost/latency tracking dashboards.

## Skills Demonstrated
- Retrieval-augmented generation system design
- Vector database usage and embedding pipelines
- Building an evaluation harness for a generative system
- Prompt engineering for grounded generation
- Basic API deployment and monitoring instincts

## Industry Relevance

Legal Tech, Healthcare Knowledge Management, Internal Enterprise Search. Organizations that sit on large bodies of documents — case law, clinical guidelines, internal policy and product docs — need systems that answer questions grounded in that material instead of an LLM's unverified memory, because a hallucinated answer in these domains carries real legal, medical, or compliance risk. Building a RAG pipeline with a real evaluation harness demonstrates the retrieval-quality and answer-faithfulness discipline these sectors require before trusting an AI system with their documents.
