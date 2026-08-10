"""Operational Knowledge Is State application flow.

State the known. Execute the consequence.
"""

from dataclasses import dataclass

from execute_knowledge_state import (
    KnowledgeFact,
    compile_knowledge_state,
    execute,
    replace_fact,
)


@dataclass(frozen=True)
class GovernedKnowledgeChange:
    """Retain the before and after states of one explicit correction."""

    original_state: object
    changed_state: object
    old_fact: KnowledgeFact
    new_fact: KnowledgeFact
    entries_replaced: int = 1
    facts_scanned: int = 0
    index_entries_copied: int = 0


@dataclass(frozen=True)
class KnowledgeIsStateFlow:
    """Facade over knowledge governance, compilation, execution, and change."""

    def govern_and_compile(self, facts):
        return compile_knowledge_state(tuple(facts))

    def execute(self, state, query):
        return execute(state, query)

    def replace(self, state, old_fact, new_fact):
        changed = replace_fact(state, old_fact, new_fact)
        return GovernedKnowledgeChange(
            state,
            changed,
            old_fact,
            new_fact,
            facts_scanned=len(state.facts),
            index_entries_copied=len(state.outgoing),
        )
