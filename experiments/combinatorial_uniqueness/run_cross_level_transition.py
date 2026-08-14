"""Human-facing composition root for Experiment 3.3."""

from .cross_level_transition_benchmark import run_experiment


def main() -> None:
    result = run_experiment()
    print(result["title"])
    print(f"Claim verdict: {result['conformity']['judgment']}")
    print(f"Stage-local resolution: {result['results']['stage_resolution_rate']:.1%}")
    print(f"Flat-control non-resolution: {result['results']['flat_control_non_resolution_rate']:.1%}")


if __name__ == "__main__":
    main()
