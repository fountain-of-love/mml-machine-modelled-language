# Using vLLM For Concept Observation

## Purpose

Use `vLLM` to serve open-weight or openly available Hugging Face models behind an OpenAI-compatible local API. This gives the observatory a repeatable way to query models for candidate concepts, candidate relations, counterexamples, and refinements.

The local server is an observation instrument. Its outputs remain candidate evidence until validated.

## Install And Authenticate

Some Hugging Face models require authentication or license acceptance before download.

```sh
hf auth login
```

Install vLLM in the active Python environment:

```sh
pip install vllm
```

The current vLLM quickstart recommends Python 3.10 through 3.13 and documents `uv`-based installation for GPU-specific backends. Use the project or machine environment that fits the target hardware.

## Serve A Model

Start an OpenAI-compatible server:

```sh
vllm serve "MODEL_ID"
```

By default, the server listens at:

```text
http://localhost:8000
```

For concept-observation work, record:

- model id;
- vLLM version;
- serve command;
- hardware;
- sampling settings;
- prompt;
- raw response; and
- timestamp.

## Query The Local Server

Use the OpenAI-compatible chat endpoint:

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "MODEL_ID",
    "messages": [
      {
        "role": "user",
        "content": "List candidate concepts related to resonance. Return JSON with labels, descriptions, and confidence."
      }
    ],
    "temperature": 0.2
  }'
```

For relation discovery:

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "MODEL_ID",
    "messages": [
      {
        "role": "user",
        "content": "Concept A: photosynthesis\nConcept B: chlorophyll\n\nWhat relationship, if any, exists between these concepts? Do not assume a relation. Return JSON with source, target, relation, directionality, confidence, limits, and counterexamples."
      }
    ],
    "temperature": 0.1
  }'
```

## Multimodal Prompt Shape

For models that support image input through the chat API, use content parts:

```sh
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "MODEL_ID",
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

Only use this shape when the served model and vLLM version support multimodal chat for that model.

## Docker Option

Some model cards expose Docker model commands:

```sh
docker model run hf.co/MODEL_ID
```

Treat Docker, pip, and custom image paths as different observation environments. Do not merge their outputs without recording the runtime path.

## Operational Notes

- Use `--api-key` only as one part of local hardening. vLLM documents that some endpoints are not protected by this option.
- If a model repository includes `generation_config.json`, vLLM may apply those generation defaults unless launched with `--generation-config vllm`.
- Keep sampling settings low-temperature for inventory work unless the probe is intentionally exploratory.
- For high-context models, lower `--max-model-len` if hardware memory is insufficient.

## Quick Links

- [vLLM documentation](https://docs.vllm.ai/)
- [vLLM quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart/)
- [vLLM OpenAI-compatible server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
- [vLLM serve CLI](https://docs.vllm.ai/en/latest/cli/serve/)
