---
title: "AI Product Capstone: RAG + Agent Integration"
track: "ai-engineer"
difficulty_tier: "advanced"
estimated_hours: 26
role: "capstone"
skill_tags: ["retrieval-augmented-generation", "agent-orchestration", "tool-use", "eval-harnesses", "api-design", "llm-observability"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: ["rag-pipeline-with-eval.md", "llm-agent-tool-use.md"]
prerequisite_learning_hours: 5
---

# AI Product Capstone: RAG + Agent Integration

## Production Workflow Mirrored
1. Combining a retrieval-grounded generation component with an
   agent that can call tools when retrieval alone isn't enough
2. A single request path: client -> API -> agent loop -> (retrieval and/or
   tool calls) -> generation -> response
3. Evaluation covering both the retrieval/generation quality and the
   agent's tool-use decisions
4. Cost/latency/guardrail observability as a required, integrated stage
5. A portfolio-level write-up connecting retrieval, tool use, evaluation,
   and observability into one coherent product story

## What You'll Build
An integrated AI product that takes the RAG pipeline you built in
`rag-pipeline-with-eval.md` and gives it to the agent from
`llm-agent-tool-use.md` as one of its tools — so the agent can decide,
per request, whether to answer from retrieved documents, call another
tool, or both — deployed behind a lightweight API with cost/latency
observability, not two side-by-side projects.

## Student-Scope Notes
- This capstone assumes you completed both prerequisite projects; it does
  not re-teach RAG mechanics or agent-loop basics — it's about wiring them
  together and closing the observability gap between them.
- "Deploy" means a local FastAPI/Flask endpoint hit with curl or a simple
  client, consistent with the RAG template's scope, not a scaled cloud
  deployment.
- Observability can reuse a stripped-down version of the logging/guardrail
  approach from `llm-app-observability-and-guardrails.md` if you built it,
  or a fresh minimal version — the required scope here is request logging,
  cost/latency tracking, and one guardrail, not the full observability
  template.

## Steps
1. Wrap your RAG pipeline's retrieval as a callable tool with the same
   input/output contract style as your other agent tools.
2. Extend the agent loop so it can choose, per request, to call the
   retrieval tool, another tool, or answer directly — and can chain them
   (e.g. retrieve, then use a second tool on the retrieved result).
3. Wrap the combined system in a single API endpoint; confirm it runs
   end-to-end for a request that needs retrieval, one that needs a
   non-retrieval tool, and one that needs both.
4. Carry over guardrails from the agent template (max steps, tool
   allowlist, input validation), extended to cover retrieval-specific
   failure modes (empty retrieval, irrelevant results).
5. Re-run (or extend) your RAG eval harness against the integrated system,
   and add at least 5 test cases that specifically exercise the agent's
   tool-choice decision (does it correctly choose to retrieve vs. use
   another tool vs. answer directly?).
6. Add request-level logging with token counts, latency, and estimated
   cost per request, plus a simple threshold-based guardrail-trip log.
7. Run the integrated system on 10-15 varied requests spanning
   retrieval-only, tool-only, and combined cases; log where the agent
   chose the wrong path.
8. Write a portfolio-level write-up connecting the pieces: architecture
   diagram, eval results (both retrieval quality and tool-choice
   accuracy), what the observability layer would tell you if the system
   started misbehaving in production, and what you'd do next for a real
   production version.

## Extension Ideas
- Add a second, independent retrieval source (e.g. a structured DB lookup
  tool alongside the vector-store RAG tool) and have the agent choose
  between them.
- Add the structured-output template's schema validation to the agent's
  final response for cases that need machine-readable output.
- Add a shadow-deployment or canary path for testing prompt/tool changes
  before they hit the primary route.
- Add automated cost-based routing (cheaper model for simple requests,
  stronger model when the agent's confidence is low).

## Skills Demonstrated
- End-to-end integration of retrieval-augmented generation with an
  agentic tool-use system
- System-level evaluation covering both generation quality and agent
  decision-making
- LLM application observability and guardrail design in an integrated
  product context
- Portfolio-level technical communication connecting retrieval, tool use,
  evaluation, and observability into one narrative

## Industry Relevance

Enterprise Software, Customer Support, Legal & Professional Services. Companies in these sectors are racing to ship AI products that combine grounded knowledge retrieval with agentic tool use — think a support copilot that answers from a knowledge base and can also file a ticket, or a research assistant that pulls documents and queries a database in the same session. Shipping this kind of integrated system, with observability that shows what it costs and where it breaks, is exactly what separates a demo from a product a company can actually put in front of customers.
