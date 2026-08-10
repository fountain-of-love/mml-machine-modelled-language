"""Compare semantic representations through the operational application flow."""

from activate_grounded_focus import SemanticFocus, SemanticGrounding
from words_carry_weight import WordsCarryWeightFlow


def sum_activation(activation, identities):
    return sum(activation.weight_for(identity) for identity in identities)


def compare_representations(experiment, strategy=None):
    flow = WordsCarryWeightFlow(strategy) if strategy else WordsCarryWeightFlow()
    sentences = tuple(experiment["sentences"])
    semantic_groundings = tuple(
        SemanticGrounding(
            sentence_index=int(record["sentence_index"]),
            surface_identity=record["surface_identity"],
            grounded_identity=record["grounded_identity"],
        )
        for record in experiment["semantic_groundings"]
    )
    original_model = flow.ground_and_compile(sentences)
    grounded_model = flow.ground_and_compile(sentences, semantic_groundings)

    original_query = experiment["original_query"]
    original_result = flow.focus_and_activate(original_model, original_query)
    result = {
        "original": {
            "identity": original_result.focused_identity,
            "activation": original_result.activation,
            "contexts": {
                name: sum_activation(original_result.activation, identities)
                for name, identities in experiment["contexts"].items()
            },
        },
        "grounded": {},
    }

    for probe in experiment["focused_queries"]:
        semantic_focus = SemanticFocus(
            source_identity=probe["source_identity"],
            focused_identity=probe["focused_identity"],
        )
        operational_result = flow.focus_and_activate(
            grounded_model, original_query, semantic_focus
        )
        focused_identity = operational_result.focused_identity
        activation = operational_result.activation
        result["grounded"][focused_identity] = {
            "semantic_focus": operational_result.semantic_focus,
            "activation": activation,
            "primary_context": sum_activation(
                activation, experiment["contexts"][probe["primary_context"]]
            ),
            "contrast_context": sum_activation(
                activation, experiment["contexts"][probe["contrast_context"]]
            ),
        }
    return result
