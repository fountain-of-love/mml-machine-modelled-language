"""Fetch supported observatory models through the Hugging Face CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from model_registry import MODEL_SPECS, get_model_spec


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOWNLOAD_ROOT = SCRIPT_DIR / "downloads"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a supported model repository from Hugging Face."
    )
    parser.add_argument(
        "--model",
        choices=sorted(MODEL_SPECS),
        required=True,
        help="Supported model alias to download.",
    )
    parser.add_argument(
        "--download-root",
        default=str(DEFAULT_DOWNLOAD_ROOT),
        help="Directory that will receive the downloaded model files.",
    )
    parser.add_argument(
        "--local-dir-name",
        help="Optional explicit local directory name. Defaults to the alias with punctuation normalized.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved command without running it.",
    )
    return parser.parse_args()


def normalize_dir_name(alias: str) -> str:
    return alias.replace(":", "-").replace("/", "-")


def build_download_command(
    *,
    hf_executable: str,
    model_id: str,
    download_root: Path,
    local_dir_name: str,
) -> list[str]:
    local_dir = download_root / local_dir_name
    return [
        hf_executable,
        "download",
        model_id,
        "--local-dir",
        str(local_dir),
    ]


def resolve_hf_executable() -> str:
    candidates = [
        shutil.which("hf"),
        str(Path.home() / "Library/Python/3.9/bin/hf"),
        str(Path(sys.executable).resolve().parent / "hf"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit(
        "Hugging Face CLI 'hf' is not installed or not on PATH. "
        "Install 'huggingface_hub' and run 'hf auth login' first."
    )


def ensure_hf_available(hf_executable: str) -> None:
    env = dict(os.environ)
    env["PATH"] = str(Path(hf_executable).parent) + os.pathsep + env.get("PATH", "")
    try:
        subprocess.run(
            [hf_executable, "--help"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit("Unable to invoke 'hf'. Check the local CLI installation.") from exc


def main() -> int:
    args = parse_args()
    spec = get_model_spec(args.model)
    download_root = Path(args.download_root).resolve()
    local_dir_name = args.local_dir_name or normalize_dir_name(spec.alias)
    hf_executable = resolve_hf_executable()
    command = build_download_command(
        hf_executable=hf_executable,
        model_id=spec.model_id,
        download_root=download_root,
        local_dir_name=local_dir_name,
    )

    if args.dry_run:
        print(" ".join(command))
        return 0

    ensure_hf_available(hf_executable)
    download_root.mkdir(parents=True, exist_ok=True)
    print(f"Fetching {spec.alias} from {spec.source_url}")
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        return completed.returncode
    print(f"Downloaded to {download_root / local_dir_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
