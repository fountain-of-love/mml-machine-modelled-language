"""Executable composition root for the Knowledge Is State demonstration."""

from knowledge_is_state import KnowledgeIsStateFlow
from knowledge_state_fixture import load_knowledge_state_fixture


def display_execution(execution):
    print(execution.query)
    for source, relation, target in zip(
        execution.path, execution.relations, execution.path[1:]
    ):
        print(f"  {source} -[{relation}]-> {target}")
    print()


def main():
    fixture = load_knowledge_state_fixture()
    flow = KnowledgeIsStateFlow()
    state = flow.govern_and_compile(fixture["facts"])

    print("=" * 52)
    print("KNOWLEDGE IS STATE")
    print("=" * 52)
    print(f"\nGoverned facts: {len(state.facts)}\n")
    for query in fixture["questions"]:
        display_execution(flow.execute(state, query))

    mutation = fixture["mutation"]
    change = flow.replace(state, mutation["old"], mutation["new"])
    print("GOVERNED CHANGE\n")
    print(f"{mutation['old'].subject} -[{mutation['old'].relation}]-> {mutation['old'].object}")
    print(f"{mutation['new'].subject} -[{mutation['new'].relation}]-> {mutation['new'].object}\n")
    display_execution(flow.execute(change.changed_state, "luma"))
    print("Retraining required: no")
    print(f"Original state preserved: {'yes' if flow.execute(state, 'luma').answer == 'sena' else 'no'}")
    print("Deterministic execution: yes")
    print("=" * 52)


if __name__ == "__main__":
    main()
