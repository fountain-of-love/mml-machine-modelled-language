"""Shared OSCARC report layout: plain words first, guided structure, linked depth.

See docs/benchmark/oscarc-reader-first-layout.md for the rules this enforces.

Every section opens with one paragraph a non-specialist can follow, then gives
the technical detail. Fixed guidance paragraphs lead the reader from the
summary into the six OSCARC steps. Findings that deserve deeper study are
listed as *signals* linking to their own reports, instead of being appended to
this one. The layout is policy-neutral: programmes own every word of content.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_TECHNICAL_MARKERS = re.compile(r"`|\|\s|\$|\b[a-z]+_[a-z_]+\b")

BRIDGE = (
    "The rest of this report shows the evidence behind that summary in six short steps "
    "called OSCARC.{signals} It ends with the next paths worth following."
)
OSCARC_INTRO = (
    "OSCARC moves in a fixed order: what was seen (**O**), what was expected beforehand (**S**), "
    "how and in which order it was done (**C**), what was actually changed or applied (**A**), "
    "what came out (**R**), and the judgment that compares the outcome with the expectation (**C**). "
    "Each step starts in everyday words and then gives the technical detail."
)
SIGNALS_INTRO = (
    "Some findings deserve a closer look than one section can give. Each signal below is "
    "explained briefly here and studied in its own report."
)


@dataclass(frozen=True)
class Section:
    """One plain-language paragraph, followed by technical Markdown lines."""

    plain: str
    technical: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.plain.strip():
            raise ValueError("every section needs a plain-language opening paragraph")
        if _TECHNICAL_MARKERS.search(self.plain):
            raise ValueError(f"plain-language paragraph contains technical notation: {self.plain[:80]!r}")


@dataclass(frozen=True)
class Signal:
    """A finding that has its own report; ``link`` points to it."""

    title: str
    section: Section
    link: str
    link_text: str


@dataclass(frozen=True)
class OscarcReport:
    title: str
    tagline: str
    intention: Section
    executive: Section
    observation: Section
    standard: Section
    context: Section
    actions: Section
    result: Section
    conclusion: Section
    next_steps: Section
    signals: tuple[Signal, ...] = ()
    parent: tuple[str, str] | None = None  # (link text, link) for a deeper-study report
    footer: tuple[str, ...] = field(default_factory=tuple)


_OSCARC_HEADINGS = (
    ("observation", "O — Objective observation"),
    ("standard", "S — Standard, baseline, or reference model"),
    ("context", "C — Context and chronology"),
    ("actions", "A — Actions, interventions, or observed mechanisms"),
    ("result", "R — Result, effect, or measured outcome"),
    ("conclusion", "C — Comparative assessment and research conclusion"),
)


def _section(lines: list[str], heading: str, section: Section) -> None:
    lines += [heading, "", section.plain, ""]
    if section.technical:
        lines += [*section.technical, ""]


def render_oscarc_markdown(report: OscarcReport) -> str:
    """Render the standard layout; content and numbers belong to the caller."""
    lines = [f"# {report.title}", "", f"> **{report.tagline}**", ""]
    if report.parent:
        text, link = report.parent
        lines += [f"*Deeper study for [{text}]({link}).*", ""]
    _section(lines, "## Research intention", report.intention)
    _section(lines, "## Executive interpretation", report.executive)
    count = len(report.signals)
    words = ("one", "two", "three", "four", "five")
    amount = words[count - 1] if 0 < count <= len(words) else str(count)
    signal_note = (
        f" After that, {amount} signal{' points' if count == 1 else 's point'} "
        "to deeper studies in separate reports."
        if count else ""
    )
    lines += [BRIDGE.format(signals=signal_note), "", "## OSCARC", "", OSCARC_INTRO, ""]
    for attribute, heading in _OSCARC_HEADINGS:
        _section(lines, f"### {heading}", getattr(report, attribute))
    if report.signals:
        lines += ["## Signals for deeper study", "", SIGNALS_INTRO, ""]
        for number, signal in enumerate(report.signals, start=1):
            _section(lines, f"### Signal {number} — {signal.title}", signal.section)
            lines += [f"Deeper study: [{signal.link_text}]({signal.link}).", ""]
    _section(lines, "## Next paths", report.next_steps)
    lines += list(report.footer)
    return "\n".join(lines).rstrip("\n") + "\n"
