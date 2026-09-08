"""Run the bounded Experiment 4.2 navigation-strategy demonstration."""

from .navigation_strategy_benchmark import markdown_report, run_experiment


def main() -> None:
    print(markdown_report(run_experiment()))


if __name__ == "__main__":
    main()
