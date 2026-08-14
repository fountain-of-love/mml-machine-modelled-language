"""Executable composition root for the bounded Words Carry Weight demonstration."""

from .console import display_representation_comparison
from .fixture import load_experiment
from .comparison import compare_representations


def main():
    experiment = load_experiment()
    comparison = compare_representations(experiment)
    display_representation_comparison(experiment, comparison)


if __name__ == "__main__":
    main()
