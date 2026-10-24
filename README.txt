REPRODUCIBILITY PACKAGE — thesis aggregates and purposive evidence synthesis

Quick reproduction (Python 3; standard library only):
  python3 revision/tools/analyse_aggregates.py --data revision/data --output derived
  python3 -m unittest discover -s revision/tests -v

This reproduces the reported descriptive tables from the supplied CSVs. It does
not reconstruct respondents, estimate causal effects, or resolve contradictory
entry values. Table and chart values represent the same reported cohort.

The same command reproduces workbook_reanalysis.json and workbook_scores.csv
from curriculum_weighted_counts.csv (item x self-rated expertise x category).
The raw_count column treats the two punctuation variants of rather important
as code 2; stored_count retains the numeric sheet's coding. Codes are -1, 1,
0, 2, 3; weights are 1, 2, 3 (17, 15, 4 respondents; none at weight 4).
No respondent identifier or linkage across items is supplied. Published scores,
recoded scores and fixed/recomputed cutoff scenarios are distinct outputs.
workbook_item_comparison.csv and workbook_assessment.json document the audit.

The same command writes selection_scenarios.csv, item_selection_robustness.csv
and selection_sensitivity.json. They cross response coding (stored/raw label),
respondent weighting (self-rated familiarity 1-3 or equal) and the range fraction
(0.35/0.45/0.55) of the thesis cutoff rule, plus the recoded fixed-cutoff case.
These are descriptive sensitivity scenarios, not recommended selection rules;
the weights are self-ratings, not measured expertise. curriculum_item_codes.csv
gives an English translation, the source competence-framework area and a
rule-based content code for each of the 64 items (interpretive; author-checked
translations and codes are flagged in the file).

Optional audit against the restricted original curriculum workbook:
  pip install -r requirements.txt
  python3 revision/tools/assess_response_workbook.py --workbook /path/to/original.xlsx --data revision/data --output workbook_audit
This requires the original file identified by its hash in workbook_assessment.json.
It is not supplied here because it contains respondent/contact and free-text
fields. Its provenance was confirmed by the supplying author; this does not
establish ethics or consent documentation. The audit releases only aggregates.

Optional document extraction:
  pip install -r requirements.txt
  python3 revision/tools/rebuild_evidence.py --thesis-dir /path/to/thesis
The directory must contain dis_lehka.docx and dis_lehka.pdf matching the hashes in
extraction_summary.json. The analysed manuscript has a 2021 title page. A related
institutional record is dated 9 February 2022, DOI10.31812/123456789/7042; equivalence
of another downloaded version should be checked before reproducing extraction.
The original thesis and participant-level records are not included here.

Optional legacy export indexing:
Place the original newdata and new_data_2/results collections at package root;
then run:
  python3 revision/tools/index_literature.py --related-dir /path/to/related_exports
  python3 revision/tools/prepare_synthesis.py
The source exports/full texts are not redistributed. The manifest identifies
source filenames and hashes. literature_index.csv retains bibliographic metadata
and provenance, not full abstracts. Candidate discovery does not establish
eligibility or quality; only 202 titles were purposively triaged, and the selected
sources/roles are recorded in fulltext_decisions.csv. Source filenames in that
ledger refer to the internal reading audit; article sections and DOI/citation
keys provide the public locators. The Supplementary Information explains the
selection and interpretation of evidence.

Search audit: search_update_2026-10-12.json preserves the four exactly recorded
final refresh queries. search_update_2026-10-21.json records, verbatim and at
the time of running, every query and DOI lookup of the later targeted update. search_access_audit.json supplies source links and recorded
access outcomes. Earlier exploratory searches survive as internal result logs,
not a complete query history. The combined search results do not establish which
individual query returned each source; no query-level attribution is inferred.

Data dictionaries: student rows are domain x occasion x category x representation;
counts are marginal totals. comparison_eligible only flags source discrepancies,
not measurement equivalence. Curriculum rows retain Ukrainian source wording,
five response counts, reported weighted score and shading. Teacher percentages
are as printed and are not converted into individual counts. Derived percentage
columns are descriptive. A workbook with the original aggregate tables is supplied
separately as thesis_recovered.xlsx.
