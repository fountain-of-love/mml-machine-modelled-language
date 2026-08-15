import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from src.helpers.artifacts import (
    compare_artifact_pair,
    missing_paths,
    without_fields,
    write_artifact_pair,
)
from src.helpers.hashing import sha256_bytes, sha256_file
from src.helpers.json_io import canonical_json_bytes, read_json
from src.helpers.provenance import hash_named_artifacts, runtime_identity, utc_now_iso
from src.helpers.research_cli import ResearchCommand, run_research_command


class SharedHelperTests(unittest.TestCase):
    def test_hashing_supports_prefixed_and_legacy_forms(self):
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        self.assertEqual(sha256_bytes(b"abc", prefixed=False), expected)
        self.assertEqual(sha256_bytes(b"abc"), f"sha256:{expected}")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "value"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path), f"sha256:{expected}")

    def test_canonical_json_is_order_independent(self):
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')

    def test_without_fields_is_nonmutating(self):
        source = {"generated_at": "now", "nested": {"value": 1}}
        stable = without_fields(source)
        stable["nested"]["value"] = 2
        self.assertIn("generated_at", source)
        self.assertEqual(source["nested"]["value"], 1)

    def test_artifact_pair_round_trip_and_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "result.json"
            markdown_path = Path(directory) / "result.md"
            write_artifact_pair(json_path, {"generated_at": "old", "value": 1}, markdown_path, "# Report\n")

            self.assertEqual(read_json(json_path)["value"], 1)
            comparison = compare_artifact_pair(
                {"generated_at": "new", "value": 1}, "# Report\n", json_path, markdown_path
            )
            self.assertTrue(comparison.matches)

            drift = compare_artifact_pair(
                {"generated_at": "new", "value": 2}, "# Changed\n", json_path, markdown_path
            )
            self.assertFalse(drift.json_matches)
            self.assertFalse(drift.text_matches)

    def test_missing_paths_reports_every_absent_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = (Path(directory) / "one", Path(directory) / "two")
            self.assertEqual(missing_paths(paths), paths)

    def test_provenance_contract_exposes_named_runtime_and_artifact_facts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact"
            path.write_bytes(b"abc")
            self.assertTrue(utc_now_iso().endswith("+00:00"))
            self.assertEqual(runtime_identity({"numpy": "test"})["numpy"], "test")
            self.assertTrue(hash_named_artifacts({"fixture": path})["fixture"].startswith("sha256:"))

    def test_research_command_owns_mode_orchestration(self):
        events = []
        command = ResearchCommand(
            description="test",
            run=lambda: {"value": 1},
            validate=lambda result: events.append(("validate", result["value"])),
            write=lambda result: events.append(("write", result["value"])),
            check=lambda result: events.append(("check", result["value"])),
            render=lambda result: "report",
        )
        with redirect_stdout(StringIO()):
            run_research_command(command, ["--check"])
        self.assertEqual(events, [("validate", 1), ("check", 1)])


if __name__ == "__main__":
    unittest.main()
