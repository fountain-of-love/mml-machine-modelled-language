from pathlib import Path
import sys


SCRIPT_DIR = Path(
    "docs/explorations/seed-vault/movement/observatory/scripts/model_query_system"
)
sys.path.insert(0, str(SCRIPT_DIR.resolve()))

from fetch_models import build_download_command, normalize_dir_name
from model_registry import get_model_spec
from query_model import build_headers, build_payload, resolve_endpoint


def test_get_model_spec_returns_qwen_mapping():
    spec = get_model_spec("qwen3:8b")
    assert spec.model_id == "Qwen/Qwen3-8B"
    assert spec.source_url == "https://huggingface.co/Qwen/Qwen3-8B"


def test_normalize_dir_name_replaces_punctuation():
    assert normalize_dir_name("qwen3:8b") == "qwen3-8b"


def test_build_download_command_uses_local_dir():
    command = build_download_command(
        hf_executable="/usr/local/bin/hf",
        model_id="Qwen/Qwen3-8B",
        download_root=Path("/tmp/downloads"),
        local_dir_name="qwen3-8b",
    )
    assert command == [
        "/usr/local/bin/hf",
        "download",
        "Qwen/Qwen3-8B",
        "--local-dir",
        "/tmp/downloads/qwen3-8b",
    ]


def test_build_payload_uses_openai_chat_shape():
    payload = build_payload(
        backend="openai-compatible",
        model_name="swiss-ai/Apertus-v1.5-8B",
        prompt="hello",
        temperature=0.2,
        max_tokens=512,
    )
    assert payload == {
        "model": "swiss-ai/Apertus-v1.5-8B",
        "messages": [{"role": "user", "content": "hello"}],
        "temperature": 0.2,
        "max_tokens": 512,
    }


def test_build_payload_uses_anthropic_messages_shape():
    payload = build_payload(
        backend="anthropic",
        model_name="claude-example",
        prompt="hello",
        temperature=0.1,
        max_tokens=256,
    )
    assert payload == {
        "model": "claude-example",
        "messages": [{"role": "user", "content": "hello"}],
        "temperature": 0.1,
        "max_tokens": 256,
    }


def test_build_headers_for_openai_compatible_api_key():
    headers = build_headers("openai-compatible", "secret")
    assert headers == {
        "Content-Type": "application/json",
        "Authorization": "Bearer secret",
    }


def test_build_headers_for_anthropic_api_key():
    headers = build_headers("anthropic", "secret")
    assert headers == {
        "Content-Type": "application/json",
        "x-api-key": "secret",
        "anthropic-version": "2023-06-01",
    }


def test_resolve_endpoint_for_local_alias_defaults_to_vllm():
    class Args:
        base_url = None
        model = "qwen3:8b"

    assert (
        resolve_endpoint(Args(), "openai-compatible")
        == "http://localhost:8000/v1/chat/completions"
    )


def test_resolve_endpoint_for_anthropic_defaults_to_messages_api():
    class Args:
        base_url = None
        model = None

    assert resolve_endpoint(Args(), "anthropic") == "https://api.anthropic.com/v1/messages"
