---
title: "LLM Workflow on Customer Data with Evaluation"
track: "forward-deployed-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["llm-api-basics", "retrieval-augmented-generation", "eval-harnesses", "prompt-engineering", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: ["customer-data-integration.md"]
prerequisite_learning_hours: 4
---

# LLM Workflow on Customer Data with Evaluation

## Production Workflow Mirrored
1. Finding the step in a customer workflow where a language model adds
   value without unacceptable risk
2. Grounding the model in the customer's own documents and data
3. Building an evaluation set from real cases with the customer's experts
4. Measuring accuracy, failure modes, and cost before anyone relies on it
5. Putting a human review step where the evaluation says it is needed

## What You'll Build
An LLM-assisted step for your customer engagement (classifying incoming
requests, drafting responses from policy documents, extracting fields
from unstructured records, summarizing case histories) grounded via
retrieval over the customer's documents, with an evaluation set of at
least fifty real cases labeled with the customer's experts, a measured
accuracy and cost report, and a human-in-the-loop review path for
low-confidence outputs.

## Student-Scope Notes
- Use a hosted model API with the customer's agreement on data handling;
  redact or anonymize where required and document the agreement.
- Fifty labeled cases is the floor. Labeling with the customer's experts
  is the point, not a chore to skip.
- No fine-tuning; retrieval and prompting with evaluation is the scope.

## Steps
1. Pick the workflow step with the customer, write down the input, the
   desired output, the acceptable error rate, and what happens on a
   wrong answer.
2. Build the evaluation set: sample at least fifty real, representative
   inputs and have the customer's experts label the correct output, with
   disagreements resolved and recorded.
3. Build the retrieval layer over the relevant customer documents from
   your integrated data, with chunking and metadata that lets you cite
   sources.
4. Write the first prompt and run the full evaluation set, scoring with
   exact match, rubric, or model-graded criteria agreed with the
   customer.
5. Analyze failures by category, iterate on retrieval and prompting, and
   rerun. Keep a table of every version's accuracy and cost per item.
6. Add a confidence signal (self-reported, retrieval score, or agreement
   across samples) and set the threshold that routes cases to human
   review, showing the accuracy-coverage trade-off.
7. Wire the step into the internal tool from the previous template or a
   simple queue, with the review path and the cited sources visible.
8. Write the evaluation report for the customer: method, results,
   failure modes, cost, the review threshold and why, and the
   monitoring you recommend.

## Extension Ideas
- Add drift monitoring by re-evaluating monthly on new cases.
- Add structured output validation with a schema.
- Compare two models on the same evaluation set and cost.
- Add feedback capture from reviewers to grow the evaluation set.

## Skills Demonstrated
- Scoping language-model use within a real workflow and risk envelope
- Retrieval-grounded generation over customer documents
- Building and using an expert-labeled evaluation set
- Confidence-based human review design and customer-facing reporting

## Industry Relevance

Enterprise AI Vendors, Insurance, Legal and Compliance Services. Forward-deployed engineers at AI companies serving these sectors are hired to make models work on a customer's own data with measured reliability, and the evaluation report, not the demo, is what closes and renews contracts. This project produces exactly that artifact.
