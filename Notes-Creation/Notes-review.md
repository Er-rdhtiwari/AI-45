SOURCE_FILE="Disney.md"
NOTES_FOLDER="Notes"

PLAN_FILE="${NOTES_FOLDER}/review-plan.md"
PROGRESS_FILE="${NOTES_FOLDER}/review-progress.md"
ANALYSIS_FILE="${NOTES_FOLDER}/analysis.md"
COVERAGE_FILE="${NOTES_FOLDER}/coverage-report.md"

Treat `${SOURCE_FILE}` as the source of truth. Review every day-wise note in `${NOTES_FOLDER}` against its corresponding day prompt.

Do not modify `${SOURCE_FILE}` or files outside `${NOTES_FOLDER}`.

## Phase 1 — Plan and analyse

1. Read `${SOURCE_FILE}` completely.
2. Inspect all day-wise notes in `${NOTES_FOLDER}`.
3. Map every source day to its note file.
4. Create `${PLAN_FILE}` with:

   * days and topics found
   * corresponding note files
   * missing, duplicate, or unmatched files
   * review order
5. Create `${PROGRESS_FILE}` with:

```text
- [ ] Day 1 analysed
- [ ] Day 1 updated
- [ ] Day 1 validated
```

Include every source day.

6. Create `${ANALYSIS_FILE}` before modifying any note.

For each day, record:

* topics covered correctly
* missing or incomplete topics
* duplicate or misplaced content
* incorrect or unclear explanations
* missing required sections, examples, diagrams, comparisons, interview content, or checklists
* formatting and grammar issues
* correct unique content to preserve
* minimum required changes
* status: `COMPLETE`, `PARTIAL`, `MAJOR GAPS`, or `NOTE MISSING`

Do not modify notes until the full analysis is complete.

## Phase 2 — Update notes

Update affected notes one day at a time in source order.

Requirements:

* Add all missing source requirements.
* Fix incorrect, unclear, duplicate, or misplaced content.
* Preserve correct and unique existing content.
* Make only minimum necessary changes.
* Do not invent unrelated topics.
* Do not unnecessarily rewrite complete sections.
* Preserve the learning order and day-wise structure.
* Keep explanations simple, practical, production-focused, revision-friendly, and suitable for Staff AI Engineer interviews.
* Fix spelling, grammar, headings, Markdown, and technical consistency.
* Create a missing note only when that day exists in `${SOURCE_FILE}`.
* Update `${PROGRESS_FILE}` after every day.

## Phase 3 — Validate each day

Before marking a day complete, verify:

* every required section and subtopic is covered
* required examples, diagrams, comparisons, interview content, and checklists are present
* content is technically correct and under the correct day
* duplicate content is minimized
* correct existing content is preserved
* formatting and terminology are consistent
* no unrelated content was added

Fix all identified gaps before marking the day as validated.

Update `${ANALYSIS_FILE}` with the changes made and final status.

## Phase 4 — Final review

After all notes are updated:

1. Re-read `${SOURCE_FILE}`.
2. Recheck every note against its day prompt.
3. Fix remaining gaps, duplication, misplaced content, inconsistencies, and formatting issues.
4. Create `${COVERAGE_FILE}` containing:

| Day | Note file | Initial status | Modified | Final status | Remaining gaps |
| --- | --------- | -------------- | -------- | ------------ | -------------- |

Also include:

* files reviewed, modified, created, and unchanged
* missing sections added
* duplicate or misplaced content resolved
* technical and formatting issues fixed
* unmatched files
* assumptions and unresolved requirements
* overall status: `COMPLETE`, `COMPLETE WITH WARNINGS`, or `INCOMPLETE`

## Execution rules

Follow this order strictly:

1. Plan
2. Analyse all notes
3. Update notes
4. Validate each note
5. Perform final coverage review

Resume from the first incomplete item in `${PROGRESS_FILE}` if interrupted. Never claim completion while required items remain unchecked.
