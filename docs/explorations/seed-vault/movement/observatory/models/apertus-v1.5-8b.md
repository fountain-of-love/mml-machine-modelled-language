# Apertus v1.5 8B vLLM Observation Note

## Model

```text
swiss-ai/Apertus-v1.5-8B
```

Use this note to run Apertus v1.5 8B as a local concept-observation model through vLLM.

## Serve

Basic Hugging Face vLLM flow:

```sh
hf auth login
pip install vllm
vllm serve "swiss-ai/Apertus-v1.5-8B"
```

The Apertus model card also notes that upstream vLLM and Transformers support may still be in progress for some paths. For the Swiss AI prepared vLLM runtime, the model card lists:

```sh
vllm serve swiss-ai/Apertus-v1.5-8B \
  --chat-template-content-format string \
  --gpu-memory-utilization 0.6 \
  --max-model-len 262144 \
  --enable-auto-tool-choice \
  --tool-call-parser apertus
```

If memory is insufficient, lower `--max-model-len` or adjust `--gpu-memory-utilization`.

## Multimodal Smoke Probe

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "swiss-ai/Apertus-v1.5-8B",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Describe this image in one sentence."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
            }
          }
        ]
      }
    ]
  }'
```

## Concept Inventory Probe

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "swiss-ai/Apertus-v1.5-8B",
    "messages": [
      {
        "role": "user",
        "content": "Inventory candidate concepts related to capacity, resonance, and semantic movement. Return JSON with concept label, concise description, aliases, source cue, and confidence. Mark every item as candidate."
      }
    ],
    "temperature": 0.2
  }'
```

## Relation Probe

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "swiss-ai/Apertus-v1.5-8B",
    "messages": [
      {
        "role": "user",
        "content": "Concept A: resonance\nConcept B: capacity\n\nWhat relation, if any, exists between these concepts? Do not assume a relation. Return JSON with source, target, relation, directionality, confidence, explanation, limits, and counterexamples."
      }
    ],
    "temperature": 0.1
  }'
```

## Docker Option

```sh
docker model run hf.co/swiss-ai/Apertus-v1.5-8B
```

Record whether the observation came from pip vLLM, Swiss AI's prepared image, or Docker model runtime.

## Observation Boundary

Apertus outputs should be treated as candidate observations. Because the model is multilingual and multimodal, record prompt language, input modality, and runtime path before comparing its outputs with text-only models.

## Source Links

- [Apertus v1.5 8B model card](https://huggingface.co/swiss-ai/Apertus-v1.5-8B)
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
