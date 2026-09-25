# Qwen3 8B vLLM Observation Note

## Model

```text
Qwen/Qwen3-8B
```

This maps the shorthand `qwen3:8b` to the Hugging Face model id used by vLLM.

Use this note to run Qwen3 8B as a local concept-observation model through vLLM.

## Serve

```sh
hf auth login
pip install vllm
vllm serve "Qwen/Qwen3-8B"
```

For tensor parallel serving across four GPUs:

```sh
vllm serve "Qwen/Qwen3-8B" --tensor-parallel-size 4
```

Adjust `--tensor-parallel-size` to the available hardware.

## Concept Inventory Probe

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "Qwen/Qwen3-8B",
    "messages": [
      {
        "role": "user",
        "content": "Inventory candidate concepts related to semantic representation. Return JSON with concept label, concise description, aliases, and confidence. Mark every item as candidate."
      }
    ],
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 20
  }'
```

## Relation Probe

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "Qwen/Qwen3-8B",
    "messages": [
      {
        "role": "user",
        "content": "Concept A: semantic identity\nConcept B: alias\n\nWhat relation, if any, exists between these concepts? Do not assume a relation. Return JSON with source, target, relation, directionality, confidence, explanation, limits, and counterexamples."
      }
    ],
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 20
  }'
```

## Observation Boundary

Qwen3 output should be stored as model-specific observation evidence. Promote concepts or relations only after cross-prompt, inverse-direction, and cross-model checks.

## Source Links

- [Qwen3 vLLM deployment note](https://github.com/QwenLM/Qwen3/blob/main/docs/source/deployment/vllm.md)
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
