# LLM Model Query System

This system provides a small local workflow for:

- fetching supported open models from Hugging Face;
- querying those models through a local `vLLM` server;
- querying compatible remote providers when credentials and endpoints are available;
- running concept-inventory prompts; and
- running relation-discovery prompts.

Supported model aliases:

- `qwen3:8b`
- `apertus`

Remote models can also be queried without adding a registry alias by using:

- `--remote-model` with `--backend openai-compatible` for OpenAI-compatible providers and gateways;
- `--remote-model` with `--backend anthropic` for Claude-compatible Anthropic messages APIs.

## Files

- `model_registry.py` maps aliases to model ids and source URLs.
- `fetch_models.py` downloads model repositories through the Hugging Face CLI.
- `query_model.py` sends prompts either to a local OpenAI-compatible `vLLM` server or to a remote provider API.

## Example

Fetch a model:

```sh
python3 docs/explorations/seed-vault/movement/observatory/scripts/model_query_system/fetch_models.py --model qwen3:8b
```

Query a model:

```sh
python3 docs/explorations/seed-vault/movement/observatory/scripts/model_query_system/query_model.py \
  --model qwen3:8b \
  --prompt "Inventory candidate concepts related to semantic representation. Return JSON."
```

Query a remote OpenAI-compatible model:

```sh
python3 docs/explorations/seed-vault/movement/observatory/scripts/model_query_system/query_model.py \
  --remote-model "MODEL_NAME" \
  --backend openai-compatible \
  --base-url "https://PROVIDER_HOST" \
  --api-key-env OPENAI_API_KEY \
  --prompt "Explain computer programming in plain language. Return JSON with explanation, distinctions, and examples."
```

Query a Claude-style remote model:

```sh
python3 docs/explorations/seed-vault/movement/observatory/scripts/model_query_system/query_model.py \
  --remote-model "MODEL_NAME" \
  --backend anthropic \
  --api-key-env ANTHROPIC_API_KEY \
  --prompt "Explain computer programming in plain language. Return JSON with explanation, distinctions, and examples."
```

Run a relation probe:

```sh
python3 docs/explorations/seed-vault/movement/observatory/scripts/model_query_system/query_model.py \
  --model apertus \
  --relation resonance capacity
```

## Runtime Assumptions

- the model is already available locally or vLLM can access it by Hugging Face id;
- `vllm serve` is running on the selected base URL;
- Hugging Face authentication is already configured when a model requires it.
- remote providers require valid credentials and an allowed base URL or API host.
- not every provider uses the same payload semantics, so the saved source packet should record the backend as well as the model name.
