SOURCE_FILE="disney.md"
DESTINATION_FOLDER="Notes"

Read the complete `${SOURCE_FILE}` and treat it as the only source of truth for generating the study notes.

Do not modify `${SOURCE_FILE}`.

## Phase 1: Inspect and plan

Before generating any notes:

1. Read the entire source file.
2. Identify every day, topic, required section, subtopic, output-format instruction, and style instruction.
3. Create `${DESTINATION_FOLDER}` if it does not exist.
4. Create `${DESTINATION_FOLDER}/PLAN.md` containing:

   * all days found in the source
   * topic of each day
   * planned output filename for each day
   * required sections for each file
   * generation order
   * validation approach
5. Create `${DESTINATION_FOLDER}/PROGRESS.md` with a checklist like:

```text
- [ ] Day 1 planned
- [ ] Day 1 generated
- [ ] Day 1 validated
- [ ] Day 2 planned
- [ ] Day 2 generated
- [ ] Day 2 validated
```

Include every day found in `${SOURCE_FILE}`.

Do not start note generation until the plan and progress tracker are created.

## Phase 2: Generate and track

Generate the notes one day at a time, following the exact order in `${SOURCE_FILE}`.

For each day:

1. Re-read that day's complete instructions from `${SOURCE_FILE}`.
2. Generate one separate Markdown file inside `${DESTINATION_FOLDER}`.
3. Follow the requested:

   * topics and subtopics
   * output structure
   * explanation depth
   * examples
   * style instructions
4. Use simple, beginner-friendly language while maintaining Staff AI Engineer–level technical depth.
5. Include practical backend, architecture, production, reliability, security, cost, latency, evaluation, and observability perspectives wherever requested.
6. Do not skip, merge, rename, or invent topics.
7. Do not add unrelated questions or unnecessary content.
8. Keep examples consistent across related days wherever possible.
9. After completing the file, validate it against the source instructions for that day.
10. Update `${DESTINATION_FOLDER}/PROGRESS.md` immediately:

    * mark generation complete
    * mark validation complete only after checking coverage
    * add a short note for any missing or unclear requirement

Never mark a day as validated without reviewing every requested section and subtopic.

## Phase 3: Per-day coverage validation

After generating each day's file, verify:

* every required main section exists
* every requested subtopic is covered
* the required output format is followed
* the requested writing style is followed
* foundational terms are defined before advanced use
* practical examples are included where requested
* production challenges and optimization strategies are included where requested
* Staff-level or interview-oriented content is included where requested
* no source requirement was silently skipped

Fix missing coverage before moving to the next day.

## Phase 4: Final full review

After all daily files are generated:

1. Re-read `${SOURCE_FILE}` completely.
2. Review every generated note file against its corresponding source section.
3. Fix:

   * missing topics
   * incomplete explanations
   * duplicated sections
   * inconsistent terminology
   * broken learning order
   * incorrect headings
   * weak or missing examples
   * accidental additions not requested by the source
4. Confirm that all files are complete and internally consistent.

Create `${DESTINATION_FOLDER}/COVERAGE_REPORT.md` containing a table with:

| Day | Output file | Required sections | Subtopics covered | Validation status | Remaining gaps |
| --- | ----------- | ----------------: | ----------------: | ----------------- | -------------- |

Also include:

* total number of days discovered
* total number of note files generated
* files successfully validated
* missing or incomplete requirements
* assumptions made
* final overall status: `COMPLETE` or `INCOMPLETE`

Use `COMPLETE` only when every requested topic and subtopic has been verified.

## Important execution rules

* Plan first, then generate.
* Track progress after every day.
* Validate every file before moving forward.
* Perform a final end-to-end coverage review.
* Keep `${SOURCE_FILE}` read-only.
* Limit all created or modified files to `${DESTINATION_FOLDER}`.
* Do not delete existing destination files unless replacement is necessary for this task.
* Do not claim completion when unchecked items remain.
* If the task is too large for one pass, continue in manageable batches while maintaining `${DESTINATION_FOLDER}/PROGRESS.md`.
* Resume from the first incomplete checklist item if execution is interrupted.
* Do not regenerate already validated files unless the final review finds a coverage issue.

Start by reading `${SOURCE_FILE}` and creating `PLAN.md` and `PROGRESS.md`. Then proceed with generation, validation, tracking, and the final coverage review.
