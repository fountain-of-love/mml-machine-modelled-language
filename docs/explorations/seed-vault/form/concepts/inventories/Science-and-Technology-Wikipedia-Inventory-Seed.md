---
artifact: inventory-seed
status: candidate
updated: 2026-08-27
source_family: wikipedia-wikidata
---

# Science And Technology Wikipedia Inventory Seed

## Purpose

This document starts a governed concept inventory for science and technology using Wikipedia and Wikidata.

It answers two separate questions:

1. how to define which entities are relevant; and
2. how to harvest them repeatably.

The recommended answer is a hybrid:

- use Wikipedia portals and category pages to define human-curated scope;
- use Wikidata items and SPARQL to extract repeatable entity sets; and
- keep the Seed Vault as the authority that decides what becomes a concept record.

## Recommendation

The best way to define relevant entities is not to start from article pages one by one.

It is better to start from a small number of governed entity classes, then expand them through Wikidata.

Recommended harvesting order:

```text
Wikipedia scope page
  -> top-level domain branch
  -> Wikidata class or topic item
  -> SPARQL expansion
  -> candidate inventory rows
  -> Seed Vault review
```

This is more stable than browsing article trees alone, and more interpretable than querying Wikidata without a curated entry point.

## Entity Definition Rule

For the first science-and-technology inventory pass, a relevant entity should satisfy all of these conditions:

- it names a field, branch, technology, method family, or scientific object class;
- it is stable enough to appear as a reusable semantic concept;
- it is broad enough to support many downstream surface forms and relations; and
- it can be grounded in a repeatable Wikipedia or Wikidata source path.

For the first pass, prefer:

- academic disciplines;
- branches of science;
- engineering disciplines;
- technology types;
- scientific methods; and
- major scientific object classes.

Defer for later passes:

- individual scientists;
- companies;
- software products;
- institutions;
- events;
- one-off inventions;
- specific papers; and
- highly local or maintenance categories.

## Why Hybrid Beats Pure Browsing

Pure browsing through Wikipedia is good for sensemaking but weak for repeatability. Pure SPARQL is good for repeatability but weak for scoping because the class graph is uneven and can become too broad too quickly.

The best operational split is:

- `Wikipedia` decides the human-readable frontier;
- `Wikidata` supplies identifiers, aliases, sitelinks, and graph expansion; and
- `Seed Vault` decides semantic acceptance and boundary.

## Scope Anchors From Wikipedia

Wikipedia already exposes useful scope anchors.

From `Wikipedia:Contents/Portals`:

- `Science` appears under human activities and under natural and physical sciences.
- `Natural and physical sciences` includes `Biological science`, `Astronomy`, `Chemistry`, `Earth sciences`, and `Physics`.

From `Wikipedia:Contents/Categories`:

- `Natural and physical sciences` lists `Biology`, `Botany`, `Ecology`, `Health sciences`, `Medicine`, `Neuroscience`, `Zoology`, `Earth sciences`, `Atmospheric sciences`, `Geology`, `Geophysics`, `Oceanography`, `Astronomy`, `Chemistry`, and `Physics`.
- `Mathematics and logic` lists `Formal sciences`, `Mathematics`, `Logic`, `Statistics`, `Applied mathematics`, `Computational science`, `Operations research`, and `Information Theory`.
- `Technology and applied sciences` lists `Technology` and `Applied sciences` as main categories and includes `Automation`, `Biotechnology`, `Chemical engineering`, `Telecommunications`, `Control theory`, `Nanotechnology`, `Robotics`, `Computing`, `Artificial intelligence`, `Computer science`, `Information technology`, `Electronics`, and `Engineering`.

These are strong first-pass anchors because they are curated, broad, and already grouped by humans into reusable topic families.

## Relevant Entity Buckets

The first inventory should distinguish at least five buckets.

### 1. Domain Concepts

Broad top-level fields used for scoping and later relation grouping.

Examples:

- `SCIENCE`
- `TECHNOLOGY`
- `FORMAL_SCIENCE`
- `NATURAL_SCIENCE`
- `APPLIED_SCIENCE`
- `ENGINEERING`

### 2. Discipline Concepts

Reusable branches and sub-branches.

Examples:

- `BIOLOGY`
- `CHEMISTRY`
- `PHYSICS`
- `ASTRONOMY`
- `EARTH_SCIENCE`
- `MATHEMATICS`
- `STATISTICS`
- `COMPUTER_SCIENCE`
- `MATERIALS_SCIENCE`

### 3. Technology Concepts

Stable technology or applied-technology classes.

Examples:

- `ARTIFICIAL_INTELLIGENCE`
- `ROBOTICS`
- `NANOTECHNOLOGY`
- `MICROTECHNOLOGY`
- `NUCLEAR_TECHNOLOGY`
- `MEDICAL_TECHNOLOGY`
- `INFORMATION_TECHNOLOGY`

### 4. Method Concepts

Concepts that represent recurring scientific or technical procedures rather than fields.

Examples:

- `SCIENTIFIC_METHOD`
- `EXPERIMENT`
- `MEASUREMENT`
- `MODELING`
- `SIMULATION`
- `CONTROL`

### 5. Object-Class Concepts

Classes of things repeatedly referenced across science and technology.

Examples:

- `ORGANISM`
- `MOLECULE`
- `ELEMENT`
- `ENERGY`
- `MATERIAL`
- `MACHINE`
- `TOOL`
- `DATA`
- `ALGORITHM`

This last bucket should be added cautiously because some object classes belong partly to relations or operators in later layers.

## First Inventory Seed

The first seed should stay at the discipline and technology-class level. That gives high coverage without immediately exploding into millions of article instances.

| Seed label | Bucket | Source anchor | Notes |
| --- | --- | --- | --- |
| `SCIENCE` | domain | Wikipedia science / Wikidata `science` | top-level scope concept |
| `TECHNOLOGY` | domain | Wikipedia technology / Wikidata technology | top-level applied scope concept |
| `FORMAL_SCIENCE` | domain | Wikipedia mathematics and logic | useful bridge to mathematics, logic, statistics, computation |
| `NATURAL_SCIENCE` | domain | Wikipedia natural and physical sciences | parent grouping for biological and physical branches |
| `APPLIED_SCIENCE` | domain | Wikipedia technology and applied sciences | parent grouping for engineering and technology |
| `BIOLOGY` | discipline | Wikipedia categories | stable major branch |
| `BOTANY` | discipline | Wikipedia categories | biological sub-branch |
| `ECOLOGY` | discipline | Wikipedia categories and portals | branch with strong cross-domain reuse |
| `HEALTH_SCIENCE` | discipline | Wikipedia categories | useful but should stay distinct from medicine |
| `MEDICINE` | discipline | Wikipedia categories | applied scientific field |
| `NEUROSCIENCE` | discipline | Wikipedia categories | bridges biology, medicine, cognition |
| `ZOOLOGY` | discipline | Wikipedia categories | biological sub-branch |
| `EARTH_SCIENCE` | discipline | Wikipedia categories and portals | parent for geology and geophysics |
| `ATMOSPHERIC_SCIENCE` | discipline | Wikipedia categories | earth-system sub-branch |
| `GEOLOGY` | discipline | Wikipedia categories and portals | stable branch |
| `GEOPHYSICS` | discipline | Wikipedia categories and portals | hybrid physical-earth branch |
| `OCEANOGRAPHY` | discipline | Wikipedia categories | stable earth-system branch |
| `ASTRONOMY` | discipline | Wikipedia categories and portals | physical science branch |
| `CHEMISTRY` | discipline | Wikipedia categories and portals | physical science branch |
| `PHYSICS` | discipline | Wikipedia categories and portals | physical science branch |
| `MATHEMATICS` | discipline | Wikipedia mathematics and logic | foundational formal science |
| `LOGIC` | discipline | Wikipedia mathematics and logic | formal reasoning branch |
| `STATISTICS` | discipline | Wikipedia mathematics and logic | formal and applied bridge |
| `APPLIED_MATHEMATICS` | discipline | Wikipedia mathematics and logic | useful applied formal branch |
| `COMPUTATIONAL_SCIENCE` | discipline | Wikipedia mathematics and logic | bridges formal science and computing |
| `OPERATIONS_RESEARCH` | discipline | Wikipedia mathematics and logic | planning and optimization branch |
| `INFORMATION_THEORY` | discipline | Wikipedia mathematics and logic | mathematically grounded concept family |
| `AUTOMATION` | technology | Wikipedia technology and applied sciences | stable technology field |
| `BIOTECHNOLOGY` | technology | Wikipedia technology and applied sciences | applied bio-technology field |
| `CHEMICAL_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `TELECOMMUNICATIONS` | technology | Wikipedia technology and applied sciences | communications technology field |
| `CONTROL_THEORY` | discipline | Wikipedia technology and applied sciences | formal/applied bridge; keep as discipline first |
| `NANOTECHNOLOGY` | technology | Wikipedia technology and applied sciences | stable technology field |
| `ROBOTICS` | technology | Wikipedia technology and applied sciences | stable technology field |
| `COMPUTING` | domain | Wikipedia technology and applied sciences | umbrella computing family |
| `ARTIFICIAL_INTELLIGENCE` | technology | Wikipedia technology and applied sciences | strong current target domain |
| `COMPUTER_ARCHITECTURE` | discipline | Wikipedia technology and applied sciences | computing branch |
| `COMPUTER_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `COMPUTER_SCIENCE` | discipline | Wikipedia technology and applied sciences | stable core discipline |
| `COMPUTER_SECURITY` | discipline | Wikipedia technology and applied sciences | computing sub-branch |
| `EMBEDDED_SYSTEMS` | technology | Wikipedia technology and applied sciences | systems technology branch |
| `HUMAN_COMPUTER_INTERACTION` | discipline | Wikipedia technology and applied sciences | interaction and design bridge |
| `INFORMATION_SYSTEMS` | discipline | Wikipedia technology and applied sciences | organizational computing branch |
| `INFORMATION_TECHNOLOGY` | technology | Wikipedia technology and applied sciences | broad technology field |
| `ELECTRONICS` | discipline | Wikipedia technology and applied sciences | foundational technology field |
| `ENGINEERING` | domain | Wikipedia portals and categories | umbrella for engineering branches |
| `AEROSPACE_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `CIVIL_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `ELECTRICAL_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `ENVIRONMENTAL_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `MATERIALS_SCIENCE` | discipline | Wikipedia technology and applied sciences | science-engineering bridge |
| `MECHANICAL_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `SOFTWARE_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |
| `SYSTEMS_ENGINEERING` | discipline | Wikipedia technology and applied sciences | engineering branch |

## Practical Rule For Relevance

If we need a crisp rule for SPARQL selection, use this order:

1. include items that correspond to top-level Wikipedia scope anchors;
2. include their major branches when they are stable academic or technology classes;
3. exclude instances that are people, organizations, products, places, and events unless we intentionally start an instance inventory;
4. keep ambiguous items in review until their sense boundary is explicit.

This keeps the first inventory concept-heavy instead of article-heavy.

## SPARQL Strategy

Use SPARQL mainly for repeatable expansion after scope is set.

Three query patterns matter most:

### 1. Fetch direct branches of a scope concept

Use when we want the immediate children of a curated root.

```sparql
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P279 wd:Q336.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

This pattern should be adapted carefully because raw `subclass of science` can be noisy.

### 2. Fetch members of a transitive class tree

Use when we already trust the root class and want the wider closure.

```sparql
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P279* wd:Q11862829.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

In practice, this must usually be combined with extra filters because `academic discipline` is too broad by itself.

### 3. Fetch items tied to Wikipedia categories or sitelinks

Use when the human scope anchor starts from Wikipedia rather than from a single Wikidata class.

```sparql
SELECT ?item ?itemLabel ?article WHERE {
  ?article schema:about ?item ;
           schema:isPartOf <https://en.wikipedia.org/> .
  ?item wdt:P31/wdt:P279* wd:Q11862829.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 200
```

This is useful when we want only items that actually have English Wikipedia coverage.

## Important Wikidata Rule

Wikidata's own help pages emphasize the distinction between:

- `instance of (P31)` for membership; and
- `subclass of (P279)` for class hierarchy.

That distinction should drive the inventory.

For a concept inventory, we usually want classes first, not instances.

So the first science-and-technology pass should bias toward:

- `subclass of` traversals for disciplines and technology types; and
- limited `instance of` use only when the item itself is the stable concept we want.

## Suggested Harvesting Workflow

```text
1. Choose one root scope page from Wikipedia.
2. Extract 10-30 top-level branches manually.
3. Resolve each branch to a Wikidata item.
4. Expand each branch with one controlled SPARQL query.
5. Normalize duplicates and ambiguous labels.
6. Assign each row a bucket:
   domain | discipline | technology | method | object-class
7. Mark each row as candidate until boundary review is complete.
```

## Recommendation For The Next Step

The next practical move should be:

1. freeze this first-pass seed list;
2. create one structured inventory table or YAML/JSON export with stable ids, labels, bucket, source page, and Wikidata ids; and
3. run SPARQL only branch by branch, starting with `mathematics`, `natural sciences`, `engineering`, and `computing`.

That gives a controlled spiral of growth instead of one enormous undifferentiated scrape.

## Sources

- [Wikidata Query Help](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/Wikidata_Query_Help)
- [Wikidata Basic Membership Properties](https://www.wikidata.org/wiki/Help:Basic_membership_properties)
- [Wikidata Data Model](https://www.wikidata.org/wiki/Wikidata:Data_model)
- [Wikipedia Contents: Portals](https://en.wikipedia.org/wiki/Wikipedia:Contents/Portals)
- [Wikipedia Contents: Categories](https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories)
- [Wikidata: science and technology (Q34104)](https://www.wikidata.org/wiki/Q34104)

