"""Model registry for observatory query and fetch workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSpec:
    alias: str
    model_id: str
    source_url: str
    default_temperature: float
    multimodal: bool = False


MODEL_SPECS = {
    "qwen3:8b": ModelSpec(
        alias="qwen3:8b",
        model_id="Qwen/Qwen3-8B",
        source_url="https://huggingface.co/Qwen/Qwen3-8B",
        default_temperature=0.1,
    ),
    "apertus": ModelSpec(
        alias="apertus",
        model_id="swiss-ai/Apertus-v1.5-8B",
        source_url="https://huggingface.co/swiss-ai/Apertus-v1.5-8B",
        default_temperature=0.1,
        multimodal=True,
    ),
}


def get_model_spec(alias: str) -> ModelSpec:
    try:
        return MODEL_SPECS[alias]
    except KeyError as exc:
        supported = ", ".join(sorted(MODEL_SPECS))
        raise ValueError(
            f"Unknown model alias '{alias}'. Supported models: {supported}."
        ) from exc
