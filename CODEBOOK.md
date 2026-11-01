# Codebook

This codebook defines the variables in `revision/data/`, the coding schemes, and the formulae used by
`revision/tools/analyse_aggregates.py`. The instruments that produced the data are documented in
[`instruments/`](instruments/README.md).

## Coding schemes and formulae

### Curriculum survey

Each of the 64 items was rated by 36 respondents. The response labels have these codes:

| Label | English | Code |
|---|---|---|
| зовсім не важливо | not important at all | -1 |
| мало важливо | slightly important | 1 |
| утруднююсь відповісти | unable to answer | 0 |
| скоріше, важливо | rather important | 2 |
| дуже важливо | very important | 3 |

**Self-rated competence weights.** The weights are 1 for "initial ideas" (17 respondents), 2 for "familiar with
some components" (15), 3 for "deeply familiar with some components" (4) and 4 for "expert" (0).

**Weighted score.** The thesis weighted score of an item *i* is S_i = sum over respondents *r* of code_ri x weight_r.

**Stored and raw-label coding.** The export contains a second label, "скоріше важливо" (without the comma), in 63
responses to items 2.01-2.04. The workbook formula stored these as 3.
- *Stored* (`published`) coding keeps the workbook values and reproduces the thesis scores.
- *Raw-label* coding treats both spellings as 2.

**Selection cutoff.** The thesis uses a range rule: cutoff = min(S) + f x (max(S) - min(S)), with f = 0.45. For the
published scores (min 92, max 156) this gives 120.8. Thirty items meet it. The thesis's final selection of 41 items
is the shaded rows of thesis Tables 2.7-2.14 (`word_row_shading` = `F2F2F2`). Eleven of those shaded items fall
below the cutoff.

**Sensitivity scenarios.** These are descriptive scenarios, not recommendations. They cross:
- coding: stored or raw-label;
- weighting: self-rated familiarity or equal (all weights 1);
- f: 0.35, 0.45 or 0.55.

One further case applies raw-label coding to the published cutoff of 120.8. Recomputing the range rule on the
raw-label scores gives 113.15.

**Derived item statistics.**
- `favorable_n` = rather important + very important.
- `favorable_percent` = 100 x `favorable_n` / 36.
- `unable_percent` = 100 x unable / 36.
- `unweighted_sum` = sum of code x count.
- `mean_among_substantive_responses` = `unweighted_sum` / (36 - unable).

### Students

There were 45 students and eight competence domains. The thesis level bands (Table 2.27) are applied to the test
percentage:

| Level | Band |
|---|---|
| `initial` | [0, 25%) |
| `intermediate` | [25, 50%) |
| `sufficient` | [50, 75%) |
| `high` | [75, 100%] |

The entry levels come from a different instrument and a different rule (see `instruments/student_assessment.md`).
The entry and exit classifications are therefore not equivalent measures.

`sufficient_or_high_n` = sufficient + high at exit, and `percent` = 100 x n / 45.

### Teachers

There were 26 teachers. Percentages are released as printed in the thesis. They are not converted into counts.

## Files

### Respondent-level files (curriculum survey, de-identified)

**`curriculum_responses_deidentified.csv`** (raw). One row per respondent; 36 rows.

| Column | Definition |
|---|---|
| `respondent_id` | R01-R36, assigned after ordering rows by content (not submission order) |
| `self_rated_competence` | Verbatim label of the self-rating |
| `expertise_weight` | Weight 1-3 derived from the self-rating |
| `item_<id>` | Verbatim response label for item `<id>` (1.01-8.06; 64 columns) |
| `domain_<k>` | Domain-importance rating, 0-5, for domains 1-8 (see `instruments/curriculum_expert_survey.md`) |

**`curriculum_responses_coded.csv`** (processed). One row per respondent and item; 2,304 rows.

| Column | Definition |
|---|---|
| `respondent_id` | As above |
| `item_id` | As above |
| `expertise_weight` | As above |
| `response_label` | Verbatim label |
| `raw_label_code` | Code from the label, with both spellings of "rather important" = 2 |
| `stored_code` | Code stored in the workbook's numeric sheet, which reproduces the thesis |

### Curriculum aggregates

**`curriculum_ratings.csv`.** Thesis Tables 2.7-2.14; one row per item.

| Column | Definition |
|---|---|
| `domain_id` | Thesis domain 1-8 |
| `item_id` | Item identifier |
| `item_uk` | Thesis wording of the item |
| `not_important`, `slightly_important`, `unable_to_answer`, `rather_important`, `very_important` | Counts per response label |
| `n` | Number of respondents (36) |
| `favorable_n`, `favorable_percent`, `unable_percent`, `unweighted_sum`, `mean_among_substantive_responses` | Derived item statistics (see formulae above) |
| `reported_expertise_weighted_score` | S_i as printed in the thesis |
| `reported_cutoff` | 120.8 |
| `meets_reported_numeric_cutoff` | Whether S_i meets the cutoff |
| `word_row_shading` | Shading of the row in the thesis Word table; `F2F2F2` = selected |
| `source_locator` | Location of the row in the thesis |
| `limitation` | Limits on interpreting the row |

**`curriculum_weighted_counts.csv`.** Counts per item, expertise weight and code.

| Column | Definition |
|---|---|
| `item_id` | Item identifier |
| `expertise_weight` | Weight 1-3 |
| `rating_code` | Response code |
| `raw_count` | Count under raw-label coding |
| `stored_count` | Count under stored coding |

**`curriculum_item_codes.csv`.** Interpretive codes for each item.

| Column | Definition |
|---|---|
| `item_uk` | Ukrainian wording |
| `item_en` | Draft English translation |
| `cfqt_area`, `cfqt_anchor` | Corresponding area of CFQT version 1.0, with locators |
| `content_code`, `content_rule` | Rule-based content code: R1 `normative_societal`, R2 `application_or_limitation`, R3 `operational_skill`, R4 `formal_mathematical`, R5 `physical_concept`, R6 `device_technology_knowledge`. The first matching rule applies; see Supplementary Information |
| `normative_content` | Whether the item has normative content |
| `composite_item` | Whether the item bundles content that would receive different codes |
| `requires_author_verification` | `true` for every item |

**`curriculum_domain_summary.csv`.** One row per domain.

| Column | Definition |
|---|---|
| `rated_items` | Number of items in the domain |
| `numeric_cutoff_items` | Items meeting the cutoff |
| `shaded_selected_items` | Items in the thesis's final (shaded) selection |
| `favorable_min_percent`, `favorable_max_percent` | Range of favourable percentages in the domain |

**`threshold_sensitivity.csv`.** Items meeting the cutoff on the published scores, at f = 0.35, 0.45 and 0.55.

**`workbook_item_comparison.csv`.** Per item, the raw-label counts and score set beside the thesis counts and score
(`recoded_*` / `raw_*` versus `thesis_*`). It also records `source_column` in the export and whether each version
meets the fixed and recomputed cutoffs.

**`workbook_scores.csv`.** `published_score` and `recoded_score` for each item.

**`workbook_reanalysis.json`.** Coding mismatches, changed scores, cutoffs and selected counts.

**`workbook_assessment.json`.** Audit of the original export: its hash, sheets, date range, missing values,
the coding cause, and limits.

**`selection_scenarios.csv`.** One row per scenario.

| Column | Definition |
|---|---|
| `coding` | `published` or `raw_label` |
| `weighting` | `self_rated_familiarity` or `equal` |
| `rule` | `range_fraction` or `fixed_published_cutoff` |
| `range_fraction` | f |
| `min_score`, `max_score` | Range of scores under the scenario |
| `cutoff` | Resulting cutoff |
| `selected_n` | Items selected |
| `selected_and_shaded_n` | Selected items that are also in the thesis's shaded selection |
| `item_8_03_selected`, `item_6_03_selected` | Whether those items are selected |
| `factorial` | Whether the scenario is part of the 12-scenario factorial design |

**`item_selection_robustness.csv`.** For each item: published score, shading, published selection, and the number
of the 12 factorial scenarios in which it is selected.

**`selection_sensitivity.json`.** Summary of `selection_scenarios.csv` and `item_selection_robustness.csv`.

### Teacher and student aggregates

**`teacher_survey.csv`.**

| Column | Definition |
|---|---|
| `item_id` | T01-T09; the mapping to questions is in `instruments/teacher_questionnaire.md` |
| `item_en` | English statement of the item |
| `reported_percent` | Percentage as printed |
| `reported_sample` | 26 |
| `source_locator` | Page of the thesis |
| `count_reconstructed` | `false`: no counts are reconstructed from the percentages |
| `note` | Notes on interpretation |

**`student_distributions.csv`.** One row per domain, occasion, level and source.

| Column | Definition |
|---|---|
| `domain_id`, `domain` | Competence domain |
| `occasion` | `before` or `after` |
| `level` | Level band |
| `count` | Number of students |
| `reported_cohort` | 45 |
| `distribution_total` | Sum of the four levels in this source |
| `source_kind` | `table` (thesis Table 2.28) or `chart_cache` (cached chart data) |
| `source_locator` | Location in the thesis |
| `comparison_eligible` | `false` for domains 3 and 4, whose table and chart disagree |
| `interpretation` | Notes on interpretation |

**`discrepancies.csv`.** The two unresolved table/chart conflicts, with both versions. They are not repaired.

**`student_exit_summary.csv`.** Exit counts at the sufficient or high level per domain (n of 45), with a
`baseline_conflict` flag.

**`analysis_summary.json`.** Summary of these outputs.

**`extraction_summary.json`.** Hashes of the analysed thesis files and extraction counts.

### Literature and evidence synthesis

**`literature_index.csv`.** Deduplicated candidate index, 7,029 records.

| Column | Definition |
|---|---|
| `record_id` | Record identifier |
| `doi`, `year`, `title`, `authors`, `journal` | Bibliographic fields |
| `discovery_class` | Keyword rule on title and abstract: A quantum + school + education; B quantum + education; C quantum + societal terms; D societal terms + education; otherwise `not_selected_by_discovery_rule`. See `revision/tools/index_literature.py` |
| `selection_status` | Screening status |
| `provenance` | Source export files |

**`discovery_candidates.tsv`.** The 924 records in classes A-D.

**`title_triage.csv`.** The 202 class-A titles, with `decision` set to `selected_for_evidence_role` or
`not_taken_forward`, and the reason.

**`fulltext_decisions.csv`.** The evidence ledger.

| Column | Definition |
|---|---|
| `citation_key`, `doi`, `legacy_record_id` | Source identifiers |
| `role` | Role of the source in the synthesis |
| `selection` | `included_purposively`, `included_targeted_update` or `not_used_in_synthesis` |
| `access` | Access to the source |
| `source_locator` | Location of the supporting passage |
| `support` | What the source supports |
| `inference_boundary` | What the source does not establish |
| `reason` | Reason for inclusion |
| `stage` | Review stage |

**`legacy_file_manifest.json`.** The export files, with hashes, entry counts and export dates.

**`literature_summary.json`.** Record counts.

**`search_update_2026-10-12.json` and `search_update_2026-10-21.json`.** Verbatim query logs.

**`search_access_audit.json`.** Source links and recorded access outcomes.

**`thesis_recovered.xlsx`** (repository root). Workbook of the aggregate tables recovered from the thesis.
