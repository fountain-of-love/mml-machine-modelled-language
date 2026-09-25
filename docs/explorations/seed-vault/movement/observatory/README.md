# Movement Observatory

The observatory documents how open models can be queried, probed, and compared to identify candidate concepts, refine existing concepts, and discover possible relations without pretending that model outputs are established facts.

Its role is observational:

```text
open model
  -> repeatable probe
  -> raw response
  -> candidate concept or relation
  -> validation and refinement
  -> governed semantic seed
```

The observatory sits under `movement` because its first concern is relation in motion: how concepts activate one another, how candidate relations appear under probes, and how those observations can later become explicit semantic structure.

## Current Notes

- [Using vLLM For Concept Observation](vllm.md)
- [Qwen3 8B vLLM Observation Note](models/qwen3-8b.md)
- [Apertus v1.5 8B vLLM Observation Note](models/apertus-v1.5-8b.md)
- [Observatory Scripts](scripts/README.md)

## Evidence Rule

An observation is not a deposit. Store prompts, model identifiers, configuration, raw outputs, and timestamps before promoting any candidate concept or relation into reviewed Seed Vault material.
