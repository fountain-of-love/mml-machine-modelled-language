"""Animal Opposition v1: a main OSCARC report and two deeper-study reports.

Run ``make opposition-report`` to regenerate all three artifact pairs and
``make opposition-report-check`` to verify them. Every number is computed.
"""

from __future__ import annotations

import math
from dataclasses import asdict
from pathlib import Path

from experiments.semantic_representation.opposition.analysis import (
    stage_cell_types,
    stage_dimension_mixing,
    stage_encoding_loss,
    stage_evaluation,
    stage_lookup,
    stage_two_hop,
    stage_validate_learned,
)
from experiments.semantic_representation.opposition.fixture import FIXTURE_PATH, governed_matrix, load_fixture
from experiments.semantic_representation.opposition.learned import learned_relation
from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.json_io import read_json
from src.helpers.oscarc_report import OscarcReport, Section, Signal, render_oscarc_markdown
from src.helpers.provenance import utc_now_iso
from src.helpers.research_cli import ResearchCommand, run_research_command


ROOT = Path(__file__).resolve().parents[3]
RESULTS_DOCS = ROOT / "docs" / "capabilities" / "semantic-representation" / "results"
REPORT_IDS = {
    "main": "opposition-matrices-v1",
    "cell_types": "opposition-cell-types-v1",
    "two_tensions": "opposition-two-tensions-v1",
}
FIXTURE_LINK = "../../../../data/demonstration/animal_opposition_v1.json"
METHOD_LINK = "../../../benchmark/oscarc-methodology.md"
LAYOUT_LINK = "../../../benchmark/oscarc-reader-first-layout.md"


def _paths(key: str) -> tuple[Path, Path]:
    report_id = REPORT_IDS[key]
    return ROOT / "benchmark" / "results" / f"{report_id}.json", RESULTS_DOCS / f"{report_id}.md"


def _finite(value):
    """JSON has no NaN; record undefined measures as null."""
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, dict):
        return {k: _finite(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_finite(v) for v in value]
    return value


def _binary(report) -> dict:
    return {**asdict(report), "sensitivity": report.sensitivity,
            "specificity": report.specificity, "precision": report.precision}


def _verdict(criteria: dict, passing: str) -> dict:
    return {"criteria": criteria, "verdict": passing if all(criteria.values()) else "NONCONFORMANT"}


# --------------------------------------------------------------------------- measurements

def run_reports() -> dict:
    fixture = load_fixture()
    governed, learned = governed_matrix(fixture), learned_relation(fixture)
    identity = {"path": "data/demonstration/animal_opposition_v1.json",
                "sha256": sha256_file(FIXTURE_PATH), "status": fixture["status"],
                "animals": len(governed.labels)}
    generated_at = utc_now_iso()
    evaluation = stage_evaluation(governed, learned)
    composition = stage_two_hop(governed)
    loss = stage_encoding_loss(governed)
    main = {
        "report": REPORT_IDS["main"], "generated_at": generated_at, "fixture": identity,
        "lookup_cat": stage_lookup(governed, "cat"),
        "encoding_loss": loss,
        "composition": {"candidates": composition["candidates"], "conflict_count": len(composition["conflicts"])},
        "validation": stage_validate_learned(governed, learned),
        "evaluation": {
            **{k: v for k, v in evaluation.items()
               if k not in ("degree_threshold_half", "signed_threshold_zero", "three_states")},
            "degree_threshold_half": _binary(evaluation["degree_threshold_half"]),
            "signed_threshold_zero": _binary(evaluation["signed_threshold_zero"]),
            "three_states": asdict(evaluation["three_states"]),
        },
    }
    cells = {"report": REPORT_IDS["cell_types"], "generated_at": generated_at, "fixture": identity,
             "pairs": loss["pairs"], "cell_types": stage_cell_types(governed, learned)}
    tensions = {"report": REPORT_IDS["two_tensions"], "generated_at": generated_at, "fixture": identity,
                "dimension_mixing": stage_dimension_mixing(governed, fixture["relations"])}
    main["conformity"] = _main_conformity(main)
    cells["conformity"] = _cell_conformity(cells)
    tensions["conformity"] = _tension_conformity(tensions)
    main["signals"] = {
        "cell_types": {"report": REPORT_IDS["cell_types"], "verdict": cells["conformity"]["verdict"]},
        "two_tensions": {"report": REPORT_IDS["two_tensions"], "verdict": tensions["conformity"]["verdict"]},
    }
    return _finite({"main": main, "cell_types": cells, "two_tensions": tensions})


def _main_conformity(main: dict) -> dict:
    ev, loss = main["evaluation"], main["encoding_loss"]
    entropy = loss["entropy_bits"]
    return _verdict({
        "projections_lose_declared_distinctions": loss["binary_zeros_that_are_alike"] > 0,
        "entropy_grows_binary_to_signed": entropy["binary"] < entropy["three_states"] < entropy["graded_values"],
        "one_matrix_answers_both_polarities": bool(main["lookup_cat"]["signed_alike"])
        and bool(main["lookup_cat"]["signed_opposites"]),
        "composition_only_proposes": all(
            c["status"] == "CANDIDATE_NOT_GOVERNED" for c in main["composition"]["candidates"]),
        "linear_rescaling_preserves_measures": (
            ev["degree_threshold_half"] == ev["signed_threshold_zero"] and ev["auc_degree"] == ev["auc_signed"]),
        "learned_relation_checked_per_cell": main["validation"]["checked_pairs"] > 0,
    }, "MECHANISM_CONFORMANT")


def _row(cells: dict, prefix: str, scale: str) -> dict:
    return next(r for r in cells["cell_types"] if r["type"].startswith(prefix) and r["scale"] == scale)


def _cell_conformity(cells: dict) -> dict:
    pairs = cells["pairs"]
    uint8, int8 = _row(cells, "uint8", "degree"), _row(cells, "int8: x127", "signed")
    return _verdict({
        "unit_scale_uint8_changes_governed_states": uint8["governed_states_kept"] < pairs,
        "signed_int8_keeps_every_governed_state": int8["governed_states_kept"] == pairs,
        "coarse_types_flatten_learned_scores": all(
            r["learned_distinct_values"] == 1 for r in cells["cell_types"] if r["levels"] <= 3),
        "float_resolves_finer_around_zero_than_half": (
            _row(cells, "float16", "signed")["resolution_at_neutral"]
            < _row(cells, "float16", "degree")["resolution_at_neutral"]),
    }, "MECHANISM_CONFORMANT")


def _tension_conformity(tensions: dict) -> dict:
    mixing = tensions["dimension_mixing"]
    return _verdict({
        "every_conflict_classified": all(c["classification"] for c in mixing["conflicts"]),
        "most_conflicts_cross_axes": mixing["conflicts_crossing_axes"] > len(mixing["conflicts"]) / 2,
        "single_axis_candidates_exist": bool(mixing["single_axis_candidates"]),
    }, "EXPLORATORY_SIGNAL")


# --------------------------------------------------------------------------- shared wording

def _criteria_lines(conformity: dict) -> tuple[str, ...]:
    return (f"**Conformity judgment: `{conformity['verdict']}`.**", "",
            *[f"- `{name}`: `{value}`" for name, value in conformity["criteria"].items()])


def _footer(key: str) -> tuple[str, ...]:
    return (f"This report follows the [OSCARC methodology]({METHOD_LINK}) and its "
            f"[reader-first layout]({LAYOUT_LINK}). The "
            f"[machine-readable artifact](../../../../benchmark/results/{REPORT_IDS[key]}.json) is authoritative.",)


def _fmt(value, digits: int = 2) -> str:
    return "n/a" if value is None else f"{value:.{digits}f}"


def _pair(a: str, b: str) -> str:
    return f"{a}–{b}"


_WORDS = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")


def _count(n: int) -> str:
    """Small counts in words, for plain-language paragraphs."""
    return _WORDS[n] if 0 <= n < len(_WORDS) else str(n)


def _and(items: list[str]) -> str:
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} and {items[-1]}"


# --------------------------------------------------------------------------- main report

def main_report(reports: dict) -> OscarcReport:
    main, cells, tensions = reports["main"], reports["cell_types"], reports["two_tensions"]
    loss, ev, val = main["encoding_loss"], main["evaluation"], main["validation"]
    pairs, entropy, states = loss["pairs"], loss["entropy_bits"], ev["three_states"]
    mixing = tensions["dimension_mixing"]
    uint8 = _row(cells, "uint8", "degree")
    wrong = val["checked_pairs"] - val["sign_agreements"]
    return OscarcReport(
        title="Animal Opposition v1 — OSCARC Report",
        tagline="The numbers in a cell are a representational decision. They decide what the mathematics can say.",
        intention=Section(
            "Some animals are enemies, like a cat and a mouse. Some are alike, like a lion and a tiger. "
            "Some never meet at all, like a bear and a lion. We wrote facts like these down as a table, "
            "one number for every pair of animals, and asked two questions. If the facts are written "
            "down clearly, can a computer answer simple questions with nothing more than school "
            "arithmetic? And can the same table be used to check what a computer has picked up on its "
            "own by reading sentences?",
            ("Technically: show with one governed relation how ordinary mathematics (lookup, negation, "
             "matrix product, comparison) becomes useful once meaning is explicit; how encoding, range, "
             "and cell type change what can be expressed and measured; and how an explicit matrix can "
             "act as a test oracle for a learned relation. Walkthrough: "
             "[Animal Opposition](../opposition-matrices.md), run with `make run-opposition`.",)),
        executive=Section(
            "The simple questions work. Ask the table for the cat's enemies and it says mouse and dog; "
            "ask who is like the cat and it says lion and tiger. The arithmetic can also suggest new "
            "ideas: the dog and the mouse share an enemy, the cat, so perhaps they are on the same side. "
            "But it sometimes suggests nonsense too, so a person still has to decide. The computer that "
            f"learned from sentences got {wrong} of {val['checked_pairs']} checked pairs wrong. For "
            "example, it thought the lion and the zebra were alike, simply because they show up in the "
            "same stories. The table caught that.",
            (f"All declared mechanism checks held (`{main['conformity']['verdict']}`). The fixture is an "
             f"authored illustration over {main['fixture']['animals']} animals, so this is a teaching "
             "result about mechanisms, not evidence about animals or any trained model. Two signals "
             "emerged and have their own reports: storage type changes meaning, and one scale holds "
             "two tensions.",)),
        observation=Section(
            "Written as plain yes or no, the table only knows that the cat and the mouse are enemies. It "
            "cannot say that the lion and the tiger are alike, or that the bear and the lion never meet: "
            "both are just no. Written with numbers from minus one to plus one, it can say all three.",
            (f"Over {pairs} distinct pairs, the binary projection kept {loss['binary_ones']} opposite pairs "
             f"and merged {loss['binary_zeros_that_are_alike']} alike pairs with "
             f"{loss['binary_zeros_that_are_neutral']} neutral ones. Information per pair: "
             f"{entropy['binary']:.2f} bits (binary), {entropy['three_states']:.2f} bits (three states), "
             f"{entropy['graded_values']:.2f} bits (graded). Two-hop composition produced "
             f"{mixing['candidates']} candidates (the {len(main['composition']['candidates'])} strongest are "
             "listed in the JSON) and "
             f"{main['composition']['conflict_count']} conflicts with governed pairs. The toy learned "
             f"relation agreed in sign with {val['sign_agreements']} of {val['checked_pairs']} governed "
             "pairs. No interpretation is made here.",)),
        standard=Section(
            "Before looking at the results we wrote down what should happen, like a checklist. The "
            "simpler tables should forget things on purpose. One table should answer both who is the "
            "cat's enemy and who is like the cat. Guesses made by arithmetic must stay guesses. Changing "
            "the scale from 0 to 1 into minus one to plus one should not, by itself, change any score.",
            (f"The reference is the governed signed matrix in [`animal_opposition_v1.json`]({FIXTURE_LINK}), "
             "with a rationale per pair and a mask separating stated neutrality from unstated pairs. The "
             "declared mechanism expectations are the conformity criteria listed under the final step.",)),
        context=Section(
            "We started with one table of numbers. From it we made the simpler yes-or-no and 0-to-1 "
            "versions. Then we asked questions about the cat, combined facts in two steps, and finally "
            "checked a version learned from 24 short sentences against the table.",
            ("```text",
             "governed signed matrix S -> binary B and degree D projections",
             "  -> lookup, polarity, and S @ S composition",
             "  -> toy learned relation from 24 sentences -> per-cell validation and IR measures",
             "```",
             "",
             "Values and sentences are authored for teaching; thresholds of ±0.5 are declared choices.")),
        actions=Section(
            "Flipping the sign of a number turns alike into enemy. So the same table answers both "
            "questions: read it as it is to find who is like the cat, read it flipped to find the cat's "
            "enemies. Combining two steps works like the saying the enemy of my enemy is my friend.",
            ("Binary and degree matrices are computed from `S`, never authored separately. Composition "
             "multiplies signs, so the opposite of an opposite becomes alike; results stay "
             "`CANDIDATE_NOT_GOVERNED`. The learned relation is the cosine of mean-centred co-occurrence "
             "vectors: a stand-in for trained weights, not an LLM.",)),
        result=Section(
            "The 0-to-1 scale and the minus-one-to-plus-one scale gave exactly the same scores for the "
            "learned version, so the range alone changed nothing. What did matter was the question we "
            "asked. Once never meet became its own answer, the learned version looked good on simple "
            f"accuracy, because it called {'every' if ev['learned_cells_in_neutral_band'] == pairs else 'almost every'} "
            "pair never meet, while it actually found "
            f"{'none' if not states['recall']['opposite'] and not states['recall']['alike'] else 'few'} "
            "of the enemies or look-alikes.",
            ("| Treatment | Sensitivity | Specificity | Precision | AUC |",
             "| --- | ---: | ---: | ---: | ---: |",
             *[f"| {name} | {_fmt(ev[key]['sensitivity'])} | {_fmt(ev[key]['specificity'])} | "
               f"{_fmt(ev[key]['precision'])} | {_fmt(ev[auc], 3)} |"
               for name, key, auc in (("Degree scale, >= 0.5", "degree_threshold_half", "auc_degree"),
                                      ("Signed scale, <= 0", "signed_threshold_zero", "auc_signed"))],
             "",
             f"Three-state task: accuracy {states['accuracy']:.2f}, macro-F1 {states['macro_f1']:.2f}; "
             f"{ev['learned_cells_in_neutral_band']}/{pairs} learned values lie in the neutral band. "
             f"Alike-versus-opposite AUC of the learned relation: {val['alike_vs_opposite_auc']:.2f}.")),
        conclusion=Section(
            "Everything behaved as expected for a demonstration. But we made up the animals' numbers "
            "ourselves, so this shows how the method works. It does not prove anything about real "
            "animals or about real artificial intelligence.",
            (*_criteria_lines(main["conformity"]), "",
             "**Evidence strength: `ILLUSTRATIVE`.** Values and sentences are authored and the learned "
             "relation is a toy, so the report establishes mechanisms and next questions only.")),
        signals=(
            Signal("The storage type changes meaning", Section(
                "How a number is stored matters, like a till that only takes whole euros. Our table puts "
                "never meet exactly in the middle. Saved as whole numbers from 0 to 255, that middle "
                f"cannot be stored, and {_count(pairs - uint8['governed_states_kept'])} pairs quietly change "
                "their meaning."), f"{REPORT_IDS['cell_types']}.md", "Opposition Cell Types v1"),
            Signal("One scale holds two tensions", Section(
                "Alike means two different things here. The dog and the mouse are on the same side "
                "because they share an enemy, the cat. The lion and the tiger are alike because they are "
                "the same kind of animal. When the arithmetic mixes these two, it makes most of its "
                f"mistakes: {mixing['conflicts_crossing_axes']} of {len(mixing['conflicts'])}."),
                f"{REPORT_IDS['two_tensions']}.md", "Opposition Two Tensions v1"),
        ),
        next_steps=Section(
            "Two next steps follow. First, give the table two separate scales: one for how two animals "
            "get along, one for how similar they are. Second, use the table as an exam for a real AI "
            "whose inside we can look at, retrain it until it passes, and keep checking that it learned "
            "rather than memorised the answers.",
            ("### Path 1 — Two axes: interaction and likeness",
             "",
             "Separate interaction from likeness, each in [-1, 1], and compose within an axis. The "
             "falsifiable prediction and protocol are in the "
             f"[two-tensions report]({REPORT_IDS['two_tensions']}.md).",
             "",
             "### Path 2 — Train, test, tune: governed matrices as tests for open weights",
             "",
             "- **Hypothesis.** A governed relation matrix can act as a test suite for a model with open "
             "weights, and a fine-tune-and-retest loop can raise held-out test scores without regressing "
             "unrelated behaviour.",
             "- **Protocol.** (1) Split governed pairs into training and held-out sets, by pair and by "
             "animal. (2) Probe an open model for the relation (embedding probe, or scored prompts with "
             "token log-probabilities) and freeze the probe. (3) Write tests with declared thresholds for "
             "sensitivity, specificity, precision, macro-F1, and AUC on held-out pairs, per axis after "
             "Path 1. (4) Fine-tune on training pairs only. (5) Re-test held-out pairs plus a regression "
             "suite. (6) Loop with a declared stopping rule and a fixed budget.",
             "- **What it measures for MML.** How much governed knowledge must be trained in versus "
             "executed explicitly. This is the Research Contract's conversion question: what still fails "
             "after tuning is worth keeping as a governed operator.",
             "- **Risks.** Testing on trained pairs measures memorisation; a probe can pass while "
             "behaviour does not change; optimising for the tests can game them; the model's compute "
             "and licence terms must be recorded.",
             "",
             "Suggested order: Path 1 first. It needs no model or compute, and Path 2's tests are cleaner "
             "per axis.")),
        footer=_footer("main"),
    )


# --------------------------------------------------------------------------- cell types report

def cell_types_report(reports: dict) -> OscarcReport:
    cells = reports["cell_types"]
    pairs, rows = cells["pairs"], cells["cell_types"]
    uint8, int8 = _row(cells, "uint8", "degree"), _row(cells, "int8: x127", "signed")
    f16s, f16d = _row(cells, "float16", "signed"), _row(cells, "float16", "degree")
    changed = pairs - uint8["governed_states_kept"]
    return OscarcReport(
        title="Opposition Cell Types v1 — OSCARC Report",
        tagline="A number can only mean what its storage can hold.",
        parent=("Animal Opposition v1", f"{REPORT_IDS['main']}.md"),
        intention=Section(
            "Every number in the animal table has to be stored somehow. Think of a supermarket till "
            "that only accepts whole euros: a price of fifty cents becomes either nothing or one euro. "
            "We asked whether the way we store the cat, dog, lion and tiger numbers can change what the "
            "table says.",
            ("Technically: store the same governed and learned relation values in nine cell types, on "
             "their natural scale (signed [-1, 1] or degree [0, 1]), read them back on the signed scale, "
             "and measure what each type preserves.",)),
        executive=Section(
            "Yes, it can. Stored as whole numbers from 0 to 255 on a 0-to-1 scale, the middle value that "
            f"means never meet cannot be stored exactly, and {_count(changed)} pairs change their meaning "
            f"just by being saved: {_and(uint8['governed_states_changed'])}. Stored the other "
            "way, with never meet at zero, every pair keeps its meaning.",
            (f"uint8 on the degree scale kept {uint8['governed_states_kept']}/{pairs} governed states; "
             f"signed int8×127 kept {int8['governed_states_kept']}/{pairs} "
             f"(`{cells['conformity']['verdict']}`).",)),
        observation=Section(
            "Some ways of storing numbers keep every pair's meaning. Others lose a few pairs, and the "
            "coarsest ones squash the learned version into a single value, so nothing useful is left.",
            (f"Nine cell types were applied to {pairs} distinct pairs. Kept states ranged from "
             f"{min(r['governed_states_kept'] for r in rows)} to {pairs}; the learned relation kept between "
             f"{min(r['learned_distinct_values'] for r in rows)} and "
             f"{max(r['learned_distinct_values'] for r in rows)} distinct values.",)),
        standard=Section(
            "We expected that storage could quietly change meaning, that the whole-number-from-0-to-255 "
            "version would be the riskiest, and that very coarse storage would wipe out the learned "
            "version's detail.",
            ("The expectations are the four conformity criteria under the final step. The float-density "
             "criterion follows from IEEE 754 and is included as a check of the measurement, not a finding.",)),
        context=Section(
            "We took the finished animal table and the learned version, saved each in nine different "
            "ways, and read them back.",
            ("Types: bool, int8 three states, int8×127, uint8×255, one-place decimal, float16 (both "
             "scales), float32, float64. The three-state classes use the ±0.5 band of the main report.",)),
        actions=Section(
            "Nothing about the animals was changed, only the way the numbers were written down. Each "
            "version was stored in its own natural range and converted back, so any difference comes "
            "from the storage alone.",
            ("`stored_as_signed()` applies a type on its own scale and maps the result back; "
             "`neutral_is_exact()` checks whether 0 (or 0.5 on the degree scale) survives storage.",)),
        result=Section(
            "Here is what each way of storing kept. Most kept everything. The 0-to-255 version on the "
            "0-to-1 scale lost the pairs sitting exactly on the line between alike and never meet. The "
            "two coarsest versions kept the table's meaning but erased all detail of the learned version.",
            ("| Type | Scale | Levels | Neutral exact | Resolution at neutral | Governed states kept | Learned AUC |",
             "| --- | --- | ---: | --- | ---: | ---: | ---: |",
             *[f"| {r['type']} | {r['scale']} | {r['levels']:,} | {r['neutral_exact']} | "
               f"{'n/a' if r['resolution_at_neutral'] is None else format(r['resolution_at_neutral'], '.1e')} | "
               f"{r['governed_states_kept']}/{pairs} | {r['learned_auc']:.3f} |" for r in rows],
             "",
             f"The uint8 failures are the band edges: degree 0.25 and 0.75 are not multiples of 1/255. "
             f"Floats are densest near zero: float16 resolves {f16s['resolution_at_neutral']:.1e} around a "
             f"neutral at 0, but {f16d['resolution_at_neutral']:.1e} around a neutral at 0.5.")),
        conclusion=Section(
            "Storage is not a detail. Putting never meet at zero, on a scale from minus one to plus one, "
            "kept every meaning in every way of storing we tried. Putting it in the middle of a 0-to-1 "
            "scale did not.",
            (*_criteria_lines(cells["conformity"]), "",
             "**Evidence strength: `ILLUSTRATIVE`.** One authored table; the effect is arithmetic and "
             "will recur wherever a band edge or neutral point is not representable.")),
        next_steps=Section(
            "Next, check the same thing on numbers that matter more: the stored weights of a real AI, "
            "which are often squeezed into small whole numbers to save memory, and the tables MML "
            "itself compiles.",
            ("- Apply the type study to compiled MML operators before choosing their storage dtype.",
             "- Repeat it for the 8-bit and 4-bit quantisation schemes used for open model weights, as "
             f"part of Path 2 in the [main report]({REPORT_IDS['main']}.md).")),
        footer=_footer("cell_types"),
    )


# --------------------------------------------------------------------------- two tensions report

def two_tensions_report(reports: dict) -> OscarcReport:
    mixing = reports["two_tensions"]["dimension_mixing"]
    conflicts = mixing["conflicts"]
    crossing = mixing["conflicts_crossing_axes"]
    same_axis = [c for c in conflicts if c["classification"] == "SAME_AXIS"]
    kinds = {kind: sum(c["classification"] == kind for c in conflicts)
             for kind in ("MIXED_PATH", "TARGET_ON_OTHER_AXIS", "SAME_AXIS")}
    single = ", ".join(f"{_pair(c['a'], c['b'])} {c['inferred']:+.2f}" for c in mixing["single_axis_candidates"])
    return OscarcReport(
        title="Opposition Two Tensions v1 — OSCARC Report",
        tagline="Alike by kind and alike by alliance are different things.",
        parent=("Animal Opposition v1", f"{REPORT_IDS['main']}.md"),
        intention=Section(
            "In the animal table, the dog and the mouse came out as on the same side, because both are "
            "enemies of the cat. The lion and the tiger are also alike, but for a different reason: they "
            "are the same kind of animal. We asked whether these are really two different things, and "
            "whether mixing them explains the arithmetic's mistakes.",
            ("Technically: tag each authored relation as interaction or likeness, decompose every "
             "two-hop composition into its contributing paths, and classify each conflict with governed "
             "knowledge by whether it crosses the two axes.",)),
        executive=Section(
            f"Mostly yes. Of the {len(conflicts)} times the arithmetic contradicted the table, {crossing} "
            "came from mixing the two kinds of alike. For example: the dog is like the wolf, the wolf "
            "hunts sheep, so the arithmetic concluded that the dog is the sheep's enemy, while sheepdogs "
            "protect sheep. The remaining mistake is different: two hunters of the same prey are rivals, "
            "not friends, and no second scale fixes that.",
            (f"{crossing}/{len(conflicts)} conflicts cross axes (`{reports['two_tensions']['conformity']['verdict']}`). "
             "The axis tags were assigned after the conflicts were seen, so this is exploratory.",)),
        observation=Section(
            "Almost every suggestion and every mistake of the two-step arithmetic passes through both "
            f"kinds of alike at once. Only {_count(len(mixing['single_axis_candidates']))} suggestions stay "
            f"within one kind: {_and([_pair(c['a'], c['b']) for c in mixing['single_axis_candidates']])}.",
            (f"{len(conflicts)} conflicts and {mixing['candidates']} candidates; "
             f"{mixing['candidates_mostly_mixed']} candidates draw most of their magnitude from mixed paths; "
             f"single-axis candidates: {single}.",)),
        standard=Section(
            "If there really are two tensions, the mistakes should mostly come from mixing them, and "
            "the sensible suggestions should mostly stay within one.",
            ("Classification rule, declared in code before the counts were read: `MIXED_PATH` when mixed "
             "paths supply more than half the inferred magnitude; `TARGET_ON_OTHER_AXIS` when single-axis "
             "paths land on a pair governed on the other axis; otherwise `SAME_AXIS`. The tags themselves "
             "are post hoc.",)),
        context=Section(
            "After the main demonstration showed the mistakes, we labelled each fact in the table as "
            "either about getting along or about being alike, and traced every two-step suggestion back "
            "through the animals it passed.",
            ("Tags live in the fixture's `dimension` field with status `EXPLORATORY_POST_HOC`. Unlisted "
             "pairs carry no tag and contribute no paths.",)),
        actions=Section(
            "We did not change any numbers. We only split each two-step result into the routes that "
            "produced it, for example dog to wolf to sheep, and noted which kind of alike each step used.",
            ("For pair (i, j), each intermediate k contributes S[i,k]·S[k,j]; contributions are labelled "
             "by the axes of their two links.",)),
        result=Section(
            f"{_count(kinds['MIXED_PATH']).capitalize()} mistakes come from chaining the two kinds of "
            f"alike, {_count(kinds['TARGET_ON_OTHER_AXIS'])} puts a getting-along guess on a pair that is "
            f"really about being the same kind, and {_count(kinds['SAME_AXIS'])} stays within getting along.",
            ("| Pair | Inferred | Governed | Governed axis | Mixed-path share | Classification |",
             "| --- | ---: | ---: | --- | ---: | --- |",
             *[f"| {_pair(c['a'], c['b'])} | {c['inferred']:+.2f} | {c['governed']:+.1f} | {c['target_axis']} | "
               f"{c['mixed_share']:.2f} | `{c['classification']}` |" for c in conflicts])),
        conclusion=Section(
            "The idea of two tensions is a strong lead, not yet a proven fact, because we made up the "
            "labels after seeing the mistakes. The real test is the next step.",
            (*_criteria_lines(reports["two_tensions"]["conformity"]), "",
             "**Evidence strength: `EXPLORATORY`.** Post hoc tags on an authored fixture.")),
        next_steps=Section(
            "Next, give the table two separate scales, filled in fresh without looking at these mistakes, "
            "and see whether the mixing mistakes disappear while the dog and mouse suggestion survives.",
            ("### Path 1 — Two axes: interaction and likeness, each in [-1, 1]",
             "",
             "- **Hypothesis.** Two signed matrices, composed within an axis unless a declared cross-axis "
             "rule applies, remove the conflicts that come from mixing tensions without losing useful "
             "candidates.",
             f"- **Prediction (falsifiable).** The {crossing} cross-axis conflicts disappear; "
             f"{', '.join(_pair(c['a'], c['b']) for c in same_axis) or 'no conflict'} persists; the "
             f"single-axis candidates ({single}) survive unchanged. Any other outcome falsifies the "
             "two-tension reading.",
             "- **Smallest experiment.** Author both axes for the same ten animals blind to this report; "
             "build two `SignedRelationMatrix` instances; compose per axis; compare against this report.",
             "- **Follow-up.** A persisting same-axis conflict asks for relation-specific composition rules "
             "(shared prey ⇒ competition), as in the "
             "[compiled semantic operator](../../knowledge-state-execution/semantic-operator-design.md).",
             "- **Risk.** Axes fitted to these ten animals; without blind re-authoring the prediction is circular.")),
        footer=_footer("two_tensions"),
    )


# --------------------------------------------------------------------------- publication

RENDERERS = {"main": main_report, "cell_types": cell_types_report, "two_tensions": two_tensions_report}


def render(reports: dict, key: str) -> str:
    return render_oscarc_markdown(RENDERERS[key](reports))


def check_reports(reports: dict) -> None:
    failed = [f"{key}.{name}" for key, report in reports.items()
              for name, ok in report["conformity"]["criteria"].items() if not ok]
    if failed:
        raise SystemExit(f"Opposition report criteria failed: {', '.join(failed)}")


def write_reports(reports: dict) -> None:
    for key in REPORT_IDS:
        json_path, text_path = _paths(key)
        write_artifact_pair(json_path, reports[key], text_path, render(reports, key))


def check_freshness(reports: dict) -> None:
    references = {}
    for key in REPORT_IDS:
        json_path, text_path = _paths(key)
        if not json_path.exists() or not text_path.exists():
            raise SystemExit(f"{REPORT_IDS[key]} artifacts are missing; run with --write.")
        references[key] = read_json(json_path)
    for key in REPORT_IDS:
        json_path, text_path = _paths(key)
        comparison = compare_artifact_pair(
            reports[key], render(references, key), json_path, text_path, volatile_fields=("generated_at",))
        if not comparison.matches:
            raise SystemExit(f"{REPORT_IDS[key]} is stale; regenerate with --write.")


def main() -> None:
    run_research_command(ResearchCommand(
        description="Generate the Animal Opposition v1 reports.",
        run=run_reports,
        validate=check_reports,
        write=write_reports,
        check=check_freshness,
        render=lambda reports: render(reports, "main"),
    ))


if __name__ == "__main__":
    main()
