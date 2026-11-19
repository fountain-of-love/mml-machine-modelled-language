import unittest

import src
from elaborations.mml_graph import GraphModel as CompatibilityGraphModel
from src.semantic_representation.graph import GraphModel


class PublicApiTests(unittest.TestCase):
    def test_root_facade_exports_runtime_owners(self):
        self.assertIs(src.GraphModel, GraphModel)
        self.assertTrue(src.CombinatorialUniquenessFlow.__module__.startswith("src."))
        self.assertIn("GraphModel", src.__all__)
        self.assertIn("CombinatorialUniquenessFlow", src.__all__)

    def test_elaboration_graph_path_is_a_compatibility_export(self):
        self.assertIs(CompatibilityGraphModel, GraphModel)

    def test_runtime_source_has_no_outer_surface_imports(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[1] / "src"
        offenders = []
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if "from elaborations" in text or "import elaborations" in text:
                offenders.append(str(path.relative_to(root)))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
