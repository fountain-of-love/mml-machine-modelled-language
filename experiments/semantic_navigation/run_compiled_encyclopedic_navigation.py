"""Run the bounded Experiment 4.1 compiled encyclopedic navigation demonstration."""

from .compiled_encyclopedic_navigation_benchmark import markdown_report, run_experiment


def main() -> None:
    print(markdown_report(run_experiment()))


if __name__ == "__main__":
    main()
