"""Present semantic activation comparisons in a console."""


def strongest_activations(activation, top_n=8, exclude=()):
    excluded = set(exclude)
    return sorted(
        (
            (identity, weight)
            for identity, weight in activation.by_identity().items()
            if identity not in excluded
        ),
        key=lambda item: (-item[1], item[0]),
    )[:top_n]


def display_activation(label, activation, top_n=8, exclude=()):
    print(f"--- {label} ---")
    for rank, (identity, weight) in enumerate(
        strongest_activations(activation, top_n, exclude), 1
    ):
        print(f"{rank}. {identity:<16} : {weight:.4f}")
    print()


def display_representation_comparison(experiment, result):
    display_exclusions = set(experiment.get("display_exclusions", ()))
    original = result["original"]
    print("REPRESENTATION A — one ambiguous semantic identity")
    display_activation(
        f"Activation for '{original['identity']}'",
        original["activation"],
        exclude=display_exclusions | {original["identity"]},
    )
    print(
        "Context activation: "
        + ", ".join(
            f"{name}={weight:.4f}"
            for name, weight in original["contexts"].items()
        )
        + "\n"
    )

    print("REPRESENTATION B — semantically grounded identities")
    grounded_identities = set(result["grounded"])
    for identity, probe in result["grounded"].items():
        display_activation(
            f"Activation for '{identity}'",
            probe["activation"],
            exclude=display_exclusions | grounded_identities,
        )
        print(
            "Context activation: "
            f"primary={probe['primary_context']:.4f}, "
            f"contrast={probe['contrast_context']:.4f}\n"
        )
