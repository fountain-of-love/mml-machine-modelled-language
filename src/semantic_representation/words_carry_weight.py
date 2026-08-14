"""Operational Words Carry Weight application flow.

Ground the known. Focus the intended. Activate the related.
"""

from dataclasses import dataclass, field

from .activate_grounded_focus import (
    PersonalizedPageRankActivationStrategy,
    activate,
    compile_transition_model,
    focus,
    ground,
)


@dataclass(frozen=True)
class FocusedActivation:
    """Operational result retaining focus beside its activation."""

    source_identity: str
    focused_identity: str
    semantic_focus: object
    activation: object


@dataclass(frozen=True)
class WordsCarryWeightFlow:
    """Coordinate the durable construction and runtime semantic flows."""

    activation_strategy: object = field(
        default_factory=PersonalizedPageRankActivationStrategy
    )

    def ground_and_compile(self, sentences, semantic_groundings=()):
        """Ground known corpus meaning and compile its transition model."""
        source = tuple(sentences)
        grounded = ground(source, semantic_groundings) if semantic_groundings else source
        return compile_transition_model(grounded)

    def focus_and_activate(self, model, source_identity, semantic_focus=None):
        """Focus intended meaning and activate its related semantic field."""
        focused_identity = (
            focus(source_identity, semantic_focus)
            if semantic_focus is not None
            else source_identity
        )
        activation = activate(
            model, focused_identity, self.activation_strategy
        )
        return FocusedActivation(
            source_identity=source_identity,
            focused_identity=focused_identity,
            semantic_focus=semantic_focus,
            activation=activation,
        )
