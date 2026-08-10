# Benchmark v1 Relevance Rubric

The single assessor applies this rubric before viewing any system ranking. Missing query/document pairs are explicitly relevance `0`.

| Grade | Meaning |
| --- | --- |
| 0 | Irrelevant: does not support the query's information need. |
| 1 | Potentially relevant: contains a weak, ambiguous, or secondary signal. |
| 2 | Relevant: materially supports the information need but is not direct proof. |
| 3 | Directly probative: explicitly evidences the information need. |

Polysemy judgments concern the intended sense, not mere occurrence of the token `bank`. GDPR judgments concern evidence discovery only; they are not legal conclusions.

The relevance judgments and rubric are fixed before ranker changes and are not loaded during ranking. Version 1 is nevertheless a development benchmark: construction and ranking mechanics may evolve after inspecting its scores. Every such change updates manifest hashes and reference results and is intended to remain visible in Git history. A later unseen version is required for held-out validation.

## Challenge annotations

Challenge tags describe why a particular query–document pair is difficult. They are pair-specific: one document can be relevant, indirect evidence for one query and a hard negative for another. Rankers never load these annotations. Slice evaluation locates annotated pairs in the complete tier ranking; it never filters the candidate set.

| Tag | Meaning |
| --- | --- |
| `zero_query_overlap` | A relevant pair shares none of the normalized query terms. |
| `paraphrase` | The document expresses the information need using a materially different formulation. |
| `polysemy` | Correct ranking depends on resolving a word sense rather than matching its surface form. |
| `indirect_evidence` | Relevance follows from a concept or relation not stated as the query phrase. |
| `contradiction` | The document contains evidence opposing the queried condition. |
| `hard_negative` | A relevance-0 document is plausibly confusable with relevant evidence. |

A semantic tag supports a comparative claim only with at least two relevant pairs across at least two queries. Smaller slices remain visible but are reported as `INSUFFICIENT_DATA`. Hard negatives are assessed with their Top-10 intrusion rate. Challenge annotations are benchmark evidence, so edits require a manifest-hash and reference-result update.
