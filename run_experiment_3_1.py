"""Human-facing composition root for Experiment 3.1."""

from direct_combinatorial_intersection_experiment import run_experiment


def main():
    result = run_experiment()
    print(result["title"])
    print(f"Claim verdict: {result['conformity']['judgment']}")
    print(f"Generalization: {result['generalization']['status']}")
    print()
    for probe in result["treatments"]["independent"]:
        trajectory = " -> ".join(
            f"N_eff={prefix['effective_candidate_count']:.2f}"
            for prefix in probe["prefixes"]
        )
        print(f"{probe['probe_id']}: {trajectory} -> {probe['top_candidate']}")


if __name__ == "__main__":
    main()
