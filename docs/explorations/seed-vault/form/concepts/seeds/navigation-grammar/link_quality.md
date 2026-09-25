---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.link_quality
canonical_label: link_quality
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Link Quality

## Overview

Link quality is the discipline of making the right words clickable for the right reasons. It is not the same as link quantity.

In the [[Seed Vault]], link quality keeps Obsidian pages useful. A good page links load-bearing terms, preserves readability, marks intentional forward links, and supports reciprocal navigation where concepts depend on each other.

Graph links worth following: [[Semantic Hub]], [[Follow-Up Link]], [[Forward Link]], [[Reciprocal Link]], [[Load-Bearing Term]], [[Local Anchor]], and [[Graph Link]].

## Definition

Link quality is the governed fitness of links for semantic navigation, human readability, and future concept growth.

## Relation Interface

```text
(form.link_quality, is_a, form.concept)
(form.link_quality, within, form.meta)
(form.link_quality, associated_with, form.semantic_hub)
(form.link_quality, associated_with, form.follow_up_link)
(form.semantic_hub, requires, form.link_quality)
```

## Boundary

Included:

- first strong use linking
- selective link density
- reciprocal linking
- intentional forward links
- distinction between section anchors and graph links

Excluded:

- linking every noun
- decorative links
- unresolved links with no ontology purpose
- pure SEO-style linking

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Link Quality]] vs [[Link Quantity]] | More links can make navigation worse if the wrong words receive attention |
| [[Graph Link]] vs [[Local Anchor]] | Graph links grow concepts; local anchors navigate within one page |

## Sources

| Source | Role |
| --- | --- |
| [[Semantic Hub]] | Link quality contract |
| [[Concept]] | Link quality notes |

## Validation Notes

| Check | Result |
| --- | --- |
| Distinguishes quality from quantity | yes |
| Names forward and reciprocal links | yes |
| Boundary excludes decorative linking | yes |

## Open Questions

- Should link quality have measurable checks?
- Should future scripts detect unlinked load-bearing terms?
