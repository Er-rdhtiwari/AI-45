# PDF validation report

## Collection summary

- Source folder: `Notes/Week-1`
- Source pattern: `*.md`
- Expected Markdown file count: 7
- Discovered Markdown file count: 7
- Count difference: 0
- Generated note PDFs: 7
- Validated note PDFs: 7
- Note-PDF pages: 371
- Index PDF: `Day-00-Notes-Index.pdf` (5 pages, passed)
- Total generated PDFs including the index: 8
- Total validated PDFs including the index: 8
- Source lines represented in the index: 19,454
- Mermaid inventory: 0 blocks across all source files
- Unresolved rendering issues: none

## Source inventory and checksum audit

The discovery inventory was recorded before output-folder generation. Day 6 changed once during the run because the user intentionally edited its opening heading; the change was detected and incorporated. No PDF-generation or validation step wrote to a source Markdown file.

| Source Markdown filename | Initial discovery SHA-256 | Final input SHA-256 | Mermaid blocks | Difference |
| --- | --- | --- | ---: | --- |
| Day-1-role-diagnostic-python-backend-architecture-clean-code-arrays.md | `d59af5d888c4…` | `d59af5d888c4…` | 0 | No change |
| Day-2-fastapi-rest-pydantic-api-contracts-versioning-and-idempotency-strings.md | `843596d5a00a…` | `843596d5a00a…` | 0 | No change |
| Day-3-postgresql-analytical-sql-nosql-redis-and-caching-hashmap.md | `477fdf3bc12f…` | `477fdf3bc12f…` | 0 | No change |
| Day-4-async-python-concurrency-retries-testing-logging-and-debugging-two-pointers.md | `64c9be0d203e…` | `64c9be0d203e…` | 0 | No change |
| Day-5-statistics-probability-eda-and-experimentation-foundations-sliding-window.md | `5a3d9d3eaa36…` | `5a3d9d3eaa36…` | 0 | No change |
| Day-6-weekend-poc-1-finance-analytics-api-with-sql-statistics-and-caching-stack.md | `6dd963af4214…` | `c2209a92e623…` | 0 | User edit detected and incorporated |
| Day-7-week-1-revision-backend-analytics-mock-and-poc-review-queue.md | `eb2a02cf493c…` | `eb2a02cf493c…` | 0 | No change |

Initial-discovery checksum equality: 6/7. Final-snapshot integrity after regeneration and index creation: 7/7.

## Per-file generation and validation

| Source Markdown filename | Generated PDF filename | Pages | Generation status | Validation status | Formatting issue detected | Formatting adjustment applied | Mermaid rendering mode | Diagram orientation / visual reflow | Source content unchanged |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Day-1-role-diagnostic-python-backend-architecture-clean-code-arrays.md | Day-1-role-diagnostic-python-backend-architecture-clean-code-arrays.pdf | 54 | success | passed | Display and inline LaTeX math required semantic typesetting instead of literal delimiter output. | Rendered 7 display and 17 inline formulas with KaTeX; kept table headers with the first row and applied margin-safe code wrapping. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |
| Day-2-fastapi-rest-pydantic-api-contracts-versioning-and-idempotency-strings.md | Day-2-fastapi-rest-pydantic-api-contracts-versioning-and-idempotency-strings.pdf | 64 | success | passed | Long code and table content required margin-safe layout. | Applied 10.5 pt pre-wrapped code and whole-word table layout inside the 18 mm margins. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |
| Day-3-postgresql-analytical-sql-nosql-redis-and-caching-hashmap.md | Day-3-postgresql-analytical-sql-nosql-redis-and-caching-hashmap.pdf | 71 | success | passed | A wide five-column table split ordinary words during the pilot render. | Changed table wrapping to preserve whole words while retaining safe wrapping for code tokens and links. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |
| Day-4-async-python-concurrency-retries-testing-logging-and-debugging-two-pointers.md | Day-4-async-python-concurrency-retries-testing-logging-and-debugging-two-pointers.pdf | 50 | success | passed | Long concurrency/code examples required margin-safe wrapping. | Applied 10.5 pt pre-wrapped code and verified all 50 rasterized pages remained inside the safety band. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |
| Day-5-statistics-probability-eda-and-experimentation-foundations-sliding-window.md | Day-5-statistics-probability-eda-and-experimentation-foundations-sliding-window.pdf | 51 | success | passed | Raw LaTeX delimiters and commands appeared as text; inline `\(...\)` math and unescaped percentages also required print normalization. | Rendered 43 display and 62 inline formulas with KaTeX; normalized delimiters and escaped `%` only in the transient render copy; visually checked formula, percentage, and rupee-symbol pages. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |
| Day-6-weekend-poc-1-finance-analytics-api-with-sql-statistics-and-caching-stack.md | Day-6-weekend-poc-1-finance-analytics-api-with-sql-statistics-and-caching-stack.pdf | 48 | success | passed | The source opening heading was intentionally edited by the user during the run, making the earlier PDF stale. | Detected checksum change, regenerated from checksum `c2209a92…`, and revalidated all 48 pages with the updated Day 6 heading. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes from final snapshot; initial checksum changed by the user |
| Day-7-week-1-revision-backend-analytics-mock-and-poc-review-queue.md | Day-7-week-1-revision-backend-analytics-mock-and-poc-review-queue.pdf | 33 | success | passed | Wide tables and code blocks required standard margin-safe pagination. | Applied whole-word table layout, pre-wrapped code, and verified all 33 rasterized pages. | Not applicable — 0 blocks | Portrait; no Mermaid reflow | Yes |

## Validation performed

- Verified exactly one note PDF for each matching Markdown source, with the identical filename stem.
- Verified every PDF is readable, non-empty, unencrypted, A4 portrait, and has at least one page.
- Parsed every source independently and compared heading, fenced-code, table, display-math, inline-math, and Mermaid inventories with the generated HTML structure.
- Confirmed every heading sequence is preserved and every visible source block meets the PDF text-token coverage threshold.
- Checked all source special characters against PDF extraction. Day 5 included `₹`, `−`, Devanagari characters, curly quotes, ellipses, and dash variants; all were present.
- Typeset all 50 display formulas and 79 inline formulas with KaTeX. Confirmed formula counts match the Markdown inventory, no KaTeX errors occurred, and no raw `$$` delimiters or LaTeX commands leaked into the PDFs.
- Converted `\(...\)` delimiters and escaped literal percentage signs only in the transient rendering copy; source Markdown bytes remained unchanged.
- Confirmed Mermaid code fences were absent. Mermaid rendering mode, landscape pages, and visual reflow are therefore not applicable.
- Rasterized and automatically scanned all 371 note-PDF pages at 96 dpi for portrait geometry, non-empty body content, and outer safety-band violations; all passed.
- Reviewed combined contact sheets for all note pages and inspected full-resolution pages containing display formulas, inline formulas, percentages, rupee symbols, dense tables, and code.
- Confirmed the screenshot-referenced Day 5 formulas now render as readable mathematical notation with no literal markup, clipping, or overlap.
- Recomputed source checksums after note generation, after note validation, and after index validation.

## Index PDF validation

- Location: `Notes/Week-1/pdfs/Day-00-Notes-Index.pdf`
- SHA-256: `7222f1d6505369ce7e483934405e0e6da1a790d23cebaaf0834a08ebd322634a`
- Page count: 5
- Generation status: success
- Validation status: passed
- Structure: cover summary, three grouped topic-card pages, quick locator, and collection summary
- Reference style: adapted from `output/pdf/Day-00-Notes-Index.pdf` found in the sibling `DSA-Design` project
- Actual collection facts: 7 notes, 371 note-PDF pages, and 19,454 source lines
- Visual validation: all five index pages were rendered and inspected at 120–180 dpi; no clipping, overlap, or margin overflow was found
- Required-title, filename, section-heading, page-count, and summary text checks: passed

## Final status

- Markdown files discovered: 7
- Note PDFs generated: 7
- Successfully validated note PDFs: 7
- Successfully validated PDFs including the index: 8
- Index PDF validation: passed
- All Markdown files unchanged by PDF tooling: yes
- All Markdown files byte-identical to initial discovery: no — Day 6 was intentionally edited by the user and the final PDF includes that change
- Unresolved rendering issues: none
