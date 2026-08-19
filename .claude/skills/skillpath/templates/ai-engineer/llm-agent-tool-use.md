---
title: "LLM Agent with Tool Use"
track: "ai-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["agent-orchestration", "tool-use", "prompt-engineering", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: []
prerequisite_learning_hours: 6
---

# LLM Agent with Tool Use

## Production Workflow Mirrored
1. Task/goal specification for the agent
2. Tool/function definitions with clear input/output contracts
3. Agent loop: plan, call a tool, observe the result, decide next step
4. Guardrails (max steps, allowed tools, input validation before execution)
5. Failure handling (tool errors, malformed calls, infinite-loop prevention)
6. Transcript logging for debugging and evaluation

## What You'll Build
An LLM-driven agent that accomplishes a multi-step task by calling a small
set of tools/functions you define (e.g. a calculator, a web/file search, a
small database lookup), with a bounded agent loop, guardrails against
runaway or unsafe tool calls, and a logged transcript of each run you can
replay and debug.

## Student-Scope Notes
- 2-4 hand-written tools with narrow, well-typed contracts, not a large
  general-purpose tool library.
- Guardrails are simple (max steps, an allowlist of tools, basic input
  validation), not a full sandboxing/security review.
- Tasks are scoped so success/failure is easy to judge by hand (e.g. "find
  and summarize X," "compute Y and explain how"), not open-ended
  agentic workflows.

## Steps
1. Pick a small set of tasks that genuinely benefit from tool calls (e.g.
   arithmetic the model is bad at, looking something up, reading a file).
2. Define 2-4 tools with explicit function signatures/schemas.
3. Build the agent loop: prompt -> model proposes a tool call or a final
   answer -> execute tool -> feed result back -> repeat.
4. Add a max-step guardrail and an allowlist restricting which tools can be
   called.
5. Add input validation before executing a tool call (reject malformed
   arguments rather than executing them).
6. Log a full transcript per run (prompts, tool calls, tool results, final
   answer).
7. Run the agent on 10-15 varied tasks; note where it looped, picked the
   wrong tool, or hallucinated a tool call.
8. Write up: failure modes you observed and which guardrail (if any)
   caught each one.

## Extension Ideas
- Add a second agent that reviews/critiques the first agent's final answer
  before it's returned.
- Add a retrieval tool backed by a small vector store (pairs naturally with
  the RAG pipeline template).
- Add cost/latency tracking per run across tool calls.
- Try a multi-tool planning strategy (e.g. explicit plan-then-execute vs.
  interleaved reasoning-and-acting).

## Skills Demonstrated
- Agent loop design and orchestration
- Tool/function-calling contracts for LLMs
- Guardrail design for agentic systems
- Debugging agentic behavior via transcript logging
