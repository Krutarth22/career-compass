---
title: "Fine-Tuning an Open LLM with LoRA"
track: "ml-engineer"
difficulty_tier: "intermediate"
estimated_hours: 18
role: "core"
skill_tags: ["lora-finetuning", "model-training", "python"]
skill_prerequisites: ["python", "ml-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Fine-Tuning an Open LLM with LoRA

## Production Workflow Mirrored
1. Task definition & dataset curation
2. Base model selection
3. Data formatting for instruction/task tuning
4. LoRA adapter configuration (rank, target modules, learning rate)
5. Training run with checkpointing
6. Before/after evaluation on held-out examples
7. Adapter packaging for reuse (merge or keep separate from base weights)

## What You'll Build
A small open-weight LLM fine-tuned with LoRA on a custom task (e.g. a
domain-specific tone, a structured-output format, or a narrow Q&A style),
with a before/after comparison showing the adapter measurably changed model
behavior on held-out prompts.

## Student-Scope Notes
- A small open-weight base model (1B-8B parameters) run on a single GPU or
  free-tier cloud notebook, not a large frontier model or multi-GPU cluster.
- Training set is 100-500 hand-curated or lightly-synthesized examples, not
  a large-scale corpus — the point is understanding the adapter training
  loop and its levers, not squeezing out state-of-the-art quality.
- Evaluation is a small held-out prompt set scored by you (and optionally an
  LLM-as-judge pass), not a formal benchmark suite.

## Steps
1. Pick a narrow task where fine-tuning should visibly outperform prompting
   alone (e.g. a strict output schema, a specific persona, a niche domain).
2. Curate/format 100-500 training examples as instruction/response pairs.
3. Pick a small open-weight base model and load it locally or in a hosted
   notebook.
4. Configure a LoRA adapter (rank, alpha, target modules) and a training
   script/library (e.g. PEFT + Transformers).
5. Run training with checkpointing; track loss.
6. Build a held-out eval prompt set; score base model vs. fine-tuned model
   on the same prompts.
7. Save/package the adapter so it can be reloaded and applied to the base
   model independently of the training run.
8. Write up: what changed qualitatively/quantitatively, what didn't, what
   you'd try next (more data, different rank, different target modules).

## Extension Ideas
- Sweep LoRA rank/alpha and compare eval scores.
- Add an LLM-as-judge scoring pass alongside manual scoring.
- Merge the adapter into the base weights and compare inference latency
  against adapter-swapping at runtime.
- Try QLoRA to fit a larger base model into the same hardware budget.

## Skills Demonstrated
- Parameter-efficient fine-tuning (LoRA) of an LLM
- Training data curation and formatting for instruction tuning
- Before/after model evaluation methodology
- Adapter packaging and reuse
