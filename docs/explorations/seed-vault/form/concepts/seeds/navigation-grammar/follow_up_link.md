---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.follow_up_link
canonical_label: follow_up_link
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Follow-Up Link

## Overview

A follow-up link is a deliberately chosen link that gives a reader direction after an introduction or section. It says: these are the next doors worth opening.

In the [[Seed Vault]], follow-up links are how a page becomes exploratory without becoming noisy. They are especially important for [[Semantic Hub|semantic hubs]], where the goal is not only to define a concept but to help the field grow.

Graph links worth following: [[Link Quality]], [[Semantic Hub]], [[Concept Trail]], [[Discovery Path]], [[Forward Link]], and [[Navigation]].

## Definition

Follow-up link is a selective outbound link that guides the next useful traversal from a concept page.

## Relation Interface

```text
(form.follow_up_link, is_a, form.concept)
(form.follow_up_link, within, form.meta)
(form.follow_up_link, associated_with, form.link_quality)
(form.follow_up_link, enables, form.concept_trail)
(form.semantic_hub, requires, form.follow_up_link)
```

## Boundary

Included:

- links worth following after an overview
- intentionally selected next concepts
- direction-setting outbound links

Excluded:

- every inline link
- automatic backlink lists
- accidental unresolved links

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Follow-Up Link]] vs [[Forward Link]] | A follow-up link guides traversal; a forward link points to a page not yet created |
| [[Follow-Up Link]] vs [[Table Of Contents]] | A table of contents navigates the page; follow-up links navigate the graph |

## Sources

| Source | Role |
| --- | --- |
| Amazonite example page | Structural inspiration |
| [[Semantic Hub]] | Requires follow-up links |

## Validation Notes

| Check | Result |
| --- | --- |
| Distinguishes page navigation from graph navigation | yes |
| Supports semantic hub behavior | yes |

## Open Questions

- Should follow-up links be capped per section?
- Should follow-up links be typed by relation family?
