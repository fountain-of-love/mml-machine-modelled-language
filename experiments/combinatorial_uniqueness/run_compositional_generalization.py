"""Run the bounded Experiment 3.4 demonstration."""

from .compositional_generalization_benchmark import markdown_report, run_experiment


def main() -> None:
    print(markdown_report(run_experiment()))


if __name__ == "__main__":
    main()
