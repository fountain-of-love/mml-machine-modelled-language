"""Query a local vLLM OpenAI-compatible server for observatory probes."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

from model_registry import MODEL_SPECS, get_model_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query a supported observatory model through a local vLLM server."
    )
    parser.add_argument(
        "--model",
        choices=sorted(MODEL_SPECS),
        help="Supported local model alias.",
    )
    parser.add_argument(
        "--remote-model",
        help="Explicit remote model id or name when querying a non-registry provider.",
    )
    parser.add_argument(
        "--backend",
        choices=["openai-compatible", "anthropic"],
        help="Backend for --remote-model. Defaults to openai-compatible.",
    )
    parser.add_argument(
        "--base-url",
        help="Base URL for the target API. Defaults to localhost for local aliases and provider defaults for remote backends.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Sampling temperature. Defaults to the model profile setting.",
    )
    parser.add_argument(
        "--prompt",
        help="Direct prompt content for the user message.",
    )
    parser.add_argument(
        "--concept",
        metavar="SEED",
        help="Generate a standard concept-inventory prompt for one seed concept.",
    )
    parser.add_argument(
        "--relation",
        nargs=2,
        metavar=("CONCEPT_A", "CONCEPT_B"),
        help="Generate a standard relation-discovery prompt for two concepts.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=800,
        help="Maximum output tokens for remote or local chat generation.",
    )
    parser.add_argument(
        "--api-key",
        help="Explicit API key for remote providers.",
    )
    parser.add_argument(
        "--api-key-env",
        help="Environment variable name that holds the API key. Defaults per backend when omitted.",
    )
    args = parser.parse_args()
    if not args.model and not args.remote_model:
        raise SystemExit("Provide either --model or --remote-model.")
    if args.model and args.remote_model:
        raise SystemExit("Use either --model or --remote-model, not both.")
    if args.remote_model and not args.backend:
        args.backend = "openai-compatible"
    return args


def build_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.concept:
        return (
            f"Inventory candidate concepts related to {args.concept}. "
            "Return JSON with concept label, concise description, aliases, and confidence. "
            "Mark every item as candidate."
        )
    if args.relation:
        concept_a, concept_b = args.relation
        return (
            f"Concept A: {concept_a}\n"
            f"Concept B: {concept_b}\n\n"
            "What relation, if any, exists between these concepts? "
            "Do not assume a relation. "
            "Return JSON with source, target, relation, directionality, confidence, explanation, limits, and counterexamples."
        )
    raise SystemExit("Provide one of --prompt, --concept, or --relation.")


def build_payload(
    *,
    backend: str,
    model_name: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    if backend == "anthropic":
        return {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    return {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


def resolve_api_key(args: argparse.Namespace, backend: str) -> str | None:
    if args.api_key:
        return args.api_key
    if args.api_key_env:
        return os.environ.get(args.api_key_env)
    if backend == "anthropic":
        return os.environ.get("ANTHROPIC_API_KEY")
    return os.environ.get("OPENAI_API_KEY")


def resolve_endpoint(args: argparse.Namespace, backend: str) -> str:
    if args.base_url:
        base_url = args.base_url.rstrip("/")
    elif args.model:
        base_url = "http://localhost:8000"
    elif backend == "anthropic":
        base_url = "https://api.anthropic.com"
    else:
        base_url = "http://localhost:8000"

    if backend == "anthropic":
        return base_url + "/v1/messages"
    return base_url + "/v1/chat/completions"


def build_headers(backend: str, api_key: str | None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if not api_key:
        return headers
    if backend == "anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        return headers
    headers["Authorization"] = f"Bearer {api_key}"
    return headers


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"vLLM server returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(
            f"Unable to reach vLLM server at {url}. Is 'vllm serve' running?"
        ) from exc


def main() -> int:
    args = parse_args()
    if args.model:
        spec = get_model_spec(args.model)
        backend = "openai-compatible"
        model_name = spec.model_id
        temperature = (
            args.temperature if args.temperature is not None else spec.default_temperature
        )
    else:
        backend = args.backend
        model_name = args.remote_model
        temperature = args.temperature if args.temperature is not None else 0.1
    prompt = build_prompt(args)
    payload = build_payload(
        backend=backend,
        model_name=model_name,
        prompt=prompt,
        temperature=temperature,
        max_tokens=args.max_tokens,
    )
    endpoint = resolve_endpoint(args, backend)
    headers = build_headers(backend, resolve_api_key(args, backend))
    response = post_json(endpoint, payload, headers)
    print(json.dumps(response, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
