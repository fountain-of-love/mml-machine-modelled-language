"""Human-facing composition root for Experiment 3.2."""

from governed_legal_qualification_experiment import run_experiment


def main():
    result = run_experiment()
    print(result["title"])
    print(f"Claim verdict: {result['conformity']['judgment']}")
    print(f"Generalization: {result['generalization']['status']}")
    print(f"Unsupported non-resolution: {result['results']['unsupported_non_resolution_rate']:.1%}")


if __name__ == "__main__":
    main()
