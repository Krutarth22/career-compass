---
title: "Reliable Structured Output & Function Calling"
track: "ai-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["tool-use", "prompt-engineering", "api-design", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Reliable Structured Output & Function Calling

## Production Workflow Mirrored
1. Defining a strict output schema (JSON schema or typed function signature)
2. Prompting/constraining the model to emit that schema reliably
3. Validating every response against the schema before it's trusted
4. Handling malformed or partial output (retry, repair, or reject)
5. Chaining structured outputs into a downstream system (e.g. calling a
   real function with the extracted arguments)
6. Regression-testing prompt changes against a fixed set of inputs

## What You'll Build
A small pipeline that takes free-text input (e.g. a support ticket, an
invoice, a natural-language command) and reliably extracts structured,
schema-validated data from it using an LLM, with automatic handling of
malformed responses and a test suite that catches prompt regressions.

## Student-Scope Notes
- One realistic extraction task (e.g. "extract order id, item, and
  quantity from this message") rather than a general-purpose extraction
  framework.
- Validation is JSON-schema-based (or a typed library like Pydantic), not a
  custom parser.
- "Regression testing" means a fixed set of 15-20 example inputs with
  expected outputs, re-run whenever the prompt or schema changes — not a
  full CI-integrated eval suite (that's a separate template).

## Steps
1. Pick an extraction or function-calling task with a clear, checkable
   output schema.
2. Define the schema (JSON schema or a typed model) precisely, including
   required vs. optional fields and value constraints.
3. Write a prompt (or use the provider's native function-calling/tool
   mode) that gets the model to emit schema-conforming output.
4. Add response validation: parse and validate against the schema, and
   classify failures (malformed JSON, missing field, wrong type).
5. Add a repair strategy for a failed response — either a targeted retry
   prompt or a second-pass repair call — with a hard cap on retries.
6. Wire the validated output into a downstream action (a mock function
   call, a database write, or a follow-up API call).
7. Build a fixed test set of 15-20 inputs with expected outputs; write a
   script that runs them all and reports pass/fail plus which failures
   were schema violations vs. wrong values.
8. Deliberately change the prompt or schema and re-run the test set; note
   what broke and why.

## Extension Ideas
- Add multi-step extraction where one field's value determines what other
  fields are required (conditional schemas).
- Compare native function-calling/tool mode against a plain prompted-JSON
  approach on reliability and latency.
- Add a confidence/uncertainty signal the caller can use to decide whether
  to trust the extraction or escalate to a human.
- Feed extracted structured output into the agent-tool-use template as one
  of its tools.

## Skills Demonstrated
- Reliable structured output design for LLM applications
- Schema validation and failure-mode handling for generative output
- Function-calling/tool-mode API usage
- Regression testing discipline for prompt-driven systems
