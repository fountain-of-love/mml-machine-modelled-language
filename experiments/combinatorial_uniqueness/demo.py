"""Human-facing composition root for the Combinatorial Uniqueness demonstration."""

from .combined_benchmark import markdown_report, run_experiment


if __name__ == "__main__":
    print(markdown_report(run_experiment()))
