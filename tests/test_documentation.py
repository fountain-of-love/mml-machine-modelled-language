import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_kernel_does_not_import_research_instrumentation(self):
        violations = []
        for module in (ROOT / "src").rglob("*.py"):
            text = module.read_text(encoding="utf-8")
            if re.search(r"^(?:from|import)\s+experiments(?:\.|\s|$)", text, re.MULTILINE):
                violations.append(module.relative_to(ROOT).as_posix())

        self.assertEqual(violations, [])

    def test_documentation_is_consolidated_under_docs(self):
        allowed_outside_docs = {ROOT / "README.md", ROOT / "LICENSE.md"}
        misplaced = [
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*.md")
            if ROOT / "docs" not in path.parents and path not in allowed_outside_docs
        ]

        self.assertEqual(misplaced, [])

    def test_internal_markdown_links_resolve(self):
        link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
        missing = []

        for document in ROOT.rglob("*.md"):
            for target in link_pattern.findall(document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#") or target.startswith("mailto:"):
                    continue
                path = target.split("#", 1)[0]
                if path and not (document.parent / path).resolve().exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {target}")

        self.assertEqual(missing, [])

    def test_primary_surfaces_use_activation_terminology(self):
        forbidden = {
            "simulated attention",
            "trained matrix",
            "trained word matrix",
            "learned abstraction",
            "llm alternative",
            "alternative for large language models",
            "attention_diffusion",
            "context_vector",
            "group_context",
            "text_context",
            "display_context_weights",
            "score_email_against_theme",
        }
        surfaces = [
            ROOT / "README.md",
            ROOT / "docs" / "How.md",
            ROOT / "src" / "semantic_representation" / "activate_grounded_focus.py",
            ROOT / "src" / "semantic_representation" / "words_carry_weight.py",
            ROOT / "elaborations" / "mml_elaborate_corpus.py",
            ROOT / "elaborations" / "mml_legal_usecase.py",
        ]
        found = []

        for surface in surfaces:
            text = surface.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                if phrase in text:
                    found.append(f"{surface.name}: {phrase}")

        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
