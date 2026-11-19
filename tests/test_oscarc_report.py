import unittest

from src.helpers.oscarc_report import OscarcReport, Section, Signal, render_oscarc_markdown


def plain(text="A cat chases a mouse.", *technical):
    return Section(text, technical)


def report(**overrides):
    fields = dict(
        title="Study", tagline="Tagline.", intention=plain(), executive=plain(),
        observation=plain("Seen."), standard=plain("Expected."), context=plain("Order."),
        actions=plain("Done."), result=plain("Outcome.", "| a | b |"), conclusion=plain("Judged."),
        next_steps=plain("Next."),
    )
    fields.update(overrides)
    return OscarcReport(**fields)


class OscarcReportLayoutTests(unittest.TestCase):
    def test_plain_paragraph_is_required_and_kept_free_of_notation(self):
        for bad in ("", "   ", "Uses `code`.", "A table | row", "Math $x$.", "Calls stage_two_hop."):
            with self.subTest(bad), self.assertRaises(ValueError):
                Section(bad)

    def test_layout_order_is_reader_first_and_guided(self):
        text = render_oscarc_markdown(report())
        order = ["## Research intention", "## Executive interpretation", "six short steps called OSCARC",
                 "## OSCARC", "### O —", "### S —", "### C — Context", "### A —", "### R —",
                 "### C — Comparative", "## Next paths"]
        positions = [text.index(marker) for marker in order]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(text.index("Seen."), text.index("### S —"))
        self.assertNotIn("## Signals", text)

    def test_plain_paragraph_precedes_technical_detail(self):
        text = render_oscarc_markdown(report())
        self.assertLess(text.index("Outcome."), text.index("| a | b |"))

    def test_signals_link_out_and_deeper_reports_link_back(self):
        signal = Signal("Storage", plain("Whole euros only."), "deeper.md", "Deeper v1")
        text = render_oscarc_markdown(report(signals=(signal, signal)))
        self.assertIn("two signals point to deeper studies", text)
        self.assertIn("### Signal 1 — Storage", text)
        self.assertIn("Deeper study: [Deeper v1](deeper.md).", text)
        child = render_oscarc_markdown(report(parent=("Parent v1", "parent.md")))
        self.assertIn("*Deeper study for [Parent v1](parent.md).*", child)


if __name__ == "__main__":
    unittest.main()
