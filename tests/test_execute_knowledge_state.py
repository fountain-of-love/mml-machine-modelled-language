import unittest

from src.knowledge_state_execution.execute_knowledge_state import (
    KnowledgeFact,
    compile_knowledge_state,
    execute,
    replace_fact,
)
from src.knowledge_state_execution.knowledge_is_state import KnowledgeIsStateFlow
from experiments.knowledge_state_execution.fixture import load_knowledge_state_fixture


class ExecuteKnowledgeStateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = load_knowledge_state_fixture()
        self.state = compile_knowledge_state(self.fixture["facts"])

    def test_declared_composition_resolves_terminal_membership(self):
        luma = execute(self.state, "luma")
        mira = execute(self.state, "mira")

        self.assertEqual(luma.answer, "sena")
        self.assertEqual(luma.path, ("luma", "vek", "tor", "sena"))
        self.assertEqual(luma.relations, ("is-a", "is-a", "belongs-to"))
        self.assertEqual(mira.answer, "ralo")

    def test_execution_is_deterministic_and_inspectable(self):
        self.assertEqual(execute(self.state, "luma"), execute(self.state, "luma"))
        self.assertEqual(execute(self.state, "luma").edges_traversed, 3)

    def test_compiled_state_is_immutable(self):
        with self.assertRaises(TypeError):
            self.state.outgoing["luma"] = KnowledgeFact("luma", "is-a", "other")

    def test_local_replacement_preserves_original_state(self):
        mutation = self.fixture["mutation"]
        changed = replace_fact(self.state, mutation["old"], mutation["new"])

        self.assertEqual(execute(changed, "luma").answer, "nora")
        self.assertEqual(execute(self.state, "luma").answer, "sena")
        self.assertEqual(execute(changed, "mira").answer, "ralo")
        self.assertNotEqual(changed.snapshot_id, self.state.snapshot_id)

    def test_rollback_reconstructs_exact_snapshot_and_execution(self):
        mutation = self.fixture["mutation"]
        changed = replace_fact(self.state, mutation["old"], mutation["new"])
        restored = replace_fact(changed, mutation["new"], mutation["old"])

        self.assertEqual(restored.snapshot_id, self.state.snapshot_id)
        self.assertEqual(execute(restored, "luma"), execute(self.state, "luma"))

    def test_invalid_or_ambiguous_facts_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported knowledge relation"):
            compile_knowledge_state((KnowledgeFact("luma", "resembles", "vek"),))
        with self.assertRaisesRegex(ValueError, "ambiguous outgoing knowledge"):
            compile_knowledge_state((
                KnowledgeFact("luma", "is-a", "vek"),
                KnowledgeFact("luma", "belongs-to", "sena"),
            ))

    def test_cycle_and_missing_terminal_fail_closed(self):
        cycle = compile_knowledge_state((
            KnowledgeFact("luma", "is-a", "vek"),
            KnowledgeFact("vek", "is-a", "luma"),
        ))
        with self.assertRaisesRegex(ValueError, "cycle"):
            execute(cycle, "luma")

        incomplete = compile_knowledge_state((KnowledgeFact("luma", "is-a", "vek"),))
        with self.assertRaisesRegex(ValueError, "no terminal belongs-to"):
            execute(incomplete, "luma")


class KnowledgeIsStateFlowTests(unittest.TestCase):
    def test_flow_coordinates_compile_execute_and_governed_change(self):
        fixture = load_knowledge_state_fixture()
        flow = KnowledgeIsStateFlow()
        state = flow.govern_and_compile(fixture["facts"])
        change = flow.replace(
            state, fixture["mutation"]["old"], fixture["mutation"]["new"]
        )

        self.assertEqual(flow.execute(state, "luma").answer, "sena")
        self.assertEqual(flow.execute(change.changed_state, "luma").answer, "nora")
        self.assertEqual(change.entries_replaced, 1)
        self.assertEqual(change.facts_scanned, 6)
        self.assertEqual(change.index_entries_copied, 6)


if __name__ == "__main__":
    unittest.main()
