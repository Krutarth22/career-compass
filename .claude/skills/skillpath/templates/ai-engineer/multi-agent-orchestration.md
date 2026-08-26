---
title: "Multi-Agent Orchestration with Shared Tool Servers"
track: "ai-engineer"
difficulty_tier: "advanced"
estimated_hours: 18
role: "core"
skill_tags: ["agent-orchestration", "mcp-integration", "tool-use", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: ["llm-agent-tool-use.md"]
prerequisite_learning_hours: 6
---

# Multi-Agent Orchestration with Shared Tool Servers

## Production Workflow Mirrored
1. Decomposing a task across multiple specialized agents (e.g. a planner,
   a researcher, a writer) instead of one general-purpose agent
2. Defining how agents communicate: message passing, a shared scratchpad,
   or a supervisor that routes work between them
3. Exposing tools through a standard, addressable interface (an MCP-style
   tool server) so any agent in the system can discover and call the same
   tools, rather than each agent hard-coding its own
4. Coordinating turn-taking and avoiding conflicting or duplicated work
5. Guardrails scoped per-agent (which agents can call which tools) plus
   system-wide guardrails (total steps, total cost, escalation to a human)
6. Tracing a request across every agent and tool call it touched, not just
   a single agent's transcript

## What You'll Build
A small multi-agent system (2-3 agents with distinct roles, e.g. a
planner that breaks a task into subtasks, a specialist that executes them
using shared tools, and a reviewer that checks the result) that shares a
common tool server rather than each agent owning its own private tools,
with a supervisor coordinating the handoffs and a unified trace showing
the full request path across every agent.

## Student-Scope Notes
- 2-3 agents with clearly distinct roles, not a large swarm — the point is
  learning coordination and shared tooling, not scaling agent count.
- The "tool server" can be a simple local process exposing tools over a
  standard schema (MCP-style, or a hand-rolled equivalent) — you don't
  need a production MCP implementation, just the same shape: tools are
  registered once and discoverable by any agent, not copy-pasted into
  each agent's code.
- Coordination is a fixed supervisor pattern (one agent routes work to
  the others and collects results), not a fully decentralized
  negotiation protocol.

## Steps
1. Pick a task that genuinely benefits from more than one role (e.g.
   "research a topic, draft a summary, then fact-check the summary
   against the research").
2. Stand up a shared tool server: register your tools once (reuse or
   extend the tools from `llm-agent-tool-use.md` if you built it) behind
   an interface any agent can call by name, rather than embedding tool
   code in each agent.
3. Define 2-3 agents with distinct system prompts/roles and specify
   exactly which tools each is allowed to call.
4. Build a supervisor that decomposes the incoming task, assigns subtasks
   to the right agent, and passes results between them (a shared
   scratchpad or explicit message objects — pick one and justify it).
5. Add per-agent guardrails (tool allowlist, max steps) and one
   system-wide guardrail (total cost or total steps across the whole
   run, with a hard stop).
6. Add end-to-end tracing: a single request ID that follows the task
   through every agent and tool call, so you can reconstruct the full
   path after the fact.
7. Run the system on 8-10 varied tasks; note cases where agents
   duplicated work, disagreed, or one agent's output confused another.
8. Write up: why you chose this coordination pattern, where it broke
   down, and what you'd change with a 4th or 5th agent added.

## Extension Ideas
- Add a second tool server (a different domain's tools) and have the
  supervisor route to the right server per subtask.
- Add a disagreement-resolution step where the reviewer agent can send
  work back to the specialist with specific feedback, not just
  accept/reject.
- Add cost/latency tracking per agent (pairs with
  `llm-app-observability-and-guardrails.md`) so you can see which agent
  in the pipeline is the expensive one.
- Swap the fixed supervisor pattern for a peer-to-peer handoff (agents
  decide who to pass to next) and compare reliability.

## Skills Demonstrated
- Multi-agent system design and task decomposition
- Standardized, shared tool-server integration (MCP-style tool sharing)
- Coordination pattern design (supervisor/routing) for agentic systems
- Cross-agent tracing and debugging

## Industry Relevance

Enterprise Automation, Research & Knowledge Work, Developer Tools. Companies building complex AI-driven workflows — research synthesis, code review pipelines, back-office process automation — increasingly split work across specialized agents rather than one monolithic prompt, because a planner/executor/reviewer split is easier to reason about and debug than a single agent doing everything. Shared tool servers and end-to-end tracing across agents are exactly the coordination and observability patterns these teams need before trusting a multi-agent system with real work.
