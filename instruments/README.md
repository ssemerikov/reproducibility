# Instruments and data-collection procedures

The empirical data come from the 2021 dissertation study by L. V. Lehka (Kryvyi Rih State Pedagogical University):
Lehka (2021), https://doi.org/10.31812/123456789/7042, in Ukrainian. The present article is a secondary analysis.
No new data were collected for it.

| Instrument | Participants | Administered | Source of the full text | Data in this repository | Respondent-level data |
|---|---|---|---|---|---|
| [Curriculum expert survey](curriculum_expert_survey.md) | 36 respondents interested in quantum technologies (students, school teachers, researchers, university lecturers) | Online form, 20 August-13 September 2021 | Original form export (column headers); thesis Appendix B, pp. 203-218 | Item-level counts, weighted scores and selection scenarios; **de-identified responses** (`curriculum_responses_deidentified.csv`, `curriculum_responses_coded.csv`) | Released after de-identification |
| [Teacher questionnaire](teacher_questionnaire.md) | 26 informatics teachers in general secondary schools | Online form; date not stated in the thesis | Thesis Appendix V, pp. 219-222 | Percentages printed in the thesis (`teacher_survey.csv`) | Not retained |
| [Student entry test-questionnaire, exit test and level criteria](student_assessment.md) | 45 students in grades 10-11 in three Kryvyi Rih schools, in an elective course | 2020-2021, at the start and end of the course | Entry test: Appendix M, pp. 255-259. Criteria: Appendix K, pp. 243-248. Level bands: Table 2.27, p. 162. The exit test is not reproduced in the thesis | Published marginal counts per domain, occasion and level (`student_distributions.csv`) | Not retained |

**De-identification of the curriculum survey.** The original export (36 rows, 85 columns) is restricted.
`revision/tools/deidentify_curriculum_responses.py` produced the released files from it:
- **Kept:** the 64 item ratings, with their verbatim response labels; the eight domain-importance ratings (0-5);
  and the self-rated competence level.
- **Removed (12 columns):** the timestamp, the eight open questions, position, length of service, and the
  e-mail/comments field.
- **Row order:** rows are ordered by response content, not by submission time, and numbered R01-R36.

The script checks that the released rows reproduce every aggregate released earlier.
`revision/tests/test_respondent_data.py` repeats that check using only the released files.

**Consent and ethics.** The teacher questionnaire stated that completion was anonymous and contained a consent item
under the Law of Ukraine "On Personal Data Protection" (No. 2297-VI, 1 June 2010). The ethics approval and the consent
statements for the study are given in the article's declarations.

**Translations.** All English renderings in this folder, and in `curriculum_item_codes.csv`, were drafted with AI
assistance and are flagged for verification by L. V. Lehka. The Ukrainian wording is the evidence.
