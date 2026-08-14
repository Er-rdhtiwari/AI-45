# PDF Validation Report

## Collection summary

- Expected Markdown files: 10
- Discovered Markdown files: 10
- Difference from expected count: +0
- Note PDFs generated: 10
- Note PDFs validated successfully: 10
- Note PDF pages: 661
- Index PDF: `Day-00-Notes-Index.pdf` (4 pages; passed)
- Total PDFs in output folder: 11
- Source files unchanged: yes
- Fenced code/text blocks rendered: 1998
- Markdown tables rendered: 78
- Typeset math expressions: 121
- Mermaid blocks discovered: 0
- Final raster pages inspected programmatically: 661
- Raster pages with blank-body or margin-boundary issues: 0
- Unresolved rendering issues: none

## Source inventory and per-file validation

| Source Markdown | SHA-256 before/after | Mermaid inventory | Generated PDF | Pages | Generation | Validation | Formatting issue detected | Formatting adjustment applied | Mermaid mode / orientation / reflow | Source unchanged |
|---|---|---:|---|---:|---|---|---|---|---|---|
| Day-8-applied-ml-lifecycle-data-preparation-and-leakage-control-linked-list.md | `9AB3210476109CA39322DC0AB98B69247EA79087091106CEA322FD4BE9F11214` / match | 0 blocks | Day-8-applied-ml-lifecycle-data-preparation-and-leakage-control-linked-list.pdf | 85 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-9-regression-classification-metrics-thresholds-and-calibration-binary-search.md | `11CE366B8C528046939DF11469A7855AB8172BFDDE8392289AC9AA5EFF15FD95` / match | 0 blocks | Day-9-regression-classification-metrics-thresholds-and-calibration-binary-search.pdf | 93 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-10-decision-trees-random-forests-gradient-boosting-and-xgboost-concepts-recursion.md | `F9B26BEA8DE89EF0BAA4EE8DDA5DCCE4DA6AF5EA1EE18320803EE4E891E19576` / match | 0 blocks | Day-10-decision-trees-random-forests-gradient-boosting-and-xgboost-concepts-recursion.pdf | 62 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-11-feature-engineering-anomaly-detection-imbalance-explainability-and-robust-error-analysis-bfs.md | `205F52AD8A354E64B42A139F62624BD9C87B5F2BB1F3768B90D7196E6C72DDBF` / match | 0 blocks | Day-11-feature-engineering-anomaly-detection-imbalance-explainability-and-robust-error-analysis-bfs.pdf | 75 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-12-ml-evaluation-a-b-testing-bias-fairness-and-business-decisioning-dfs.md | `400A68E939C9B21069D17A62A8DA4D972C5ADAF48A7AA7235144C8DB91821493` / match | 0 blocks | Day-12-ml-evaluation-a-b-testing-bias-fairness-and-business-decisioning-dfs.pdf | 73 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-13-weekend-poc-2-explainable-finance-risk-or-anomaly-model-heap.md | `565E7F26B92E097BF138763AADFFC0514846D9CBC063D472D5697CE90D56BB33` / match | 0 blocks | Day-13-weekend-poc-2-explainable-finance-risk-or-anomaly-model-heap.pdf | 52 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-14-week-2-revision-ml-case-study-and-model-review-sorting.md | `A89A7D543E6AB2F1FF02C0C1D08FA695695C065DA283C878DD0624CD13ECD9F6` / match | 0 blocks | Day-14-week-2-revision-ml-case-study-and-model-review-sorting.pdf | 36 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-64-FinanceForecasting.md | `2C31AFE5CA2173F2FA82D2EE562679C74E2ED5BE7E2F1D9441641976C9D640CE` / match | 0 blocks | Day-64-FinanceForecasting.pdf | 65 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-65-Intelligent-Document-Processing.md | `DEE12306675F36EE3F035EAA271EE0D5BEC9742554D91559CD64E95D2327F8B6` / match | 0 blocks | Day-65-Intelligent-Document-Processing.pdf | 63 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |
| Day-66-Multi-Cloud.md | `3A435B483D849A9A8AD1551DEA4AACFBC3E89CC65D943139872EF4850E758BC8` / match | 0 blocks | Day-66-Multi-Cloud.pdf | 57 | success | passed | none | wrapped long code and table text within the A4 portrait content area | not applicable / portrait / none | yes |

## Index PDF validation

- File: `Day-00-Notes-Index.pdf`
- Page count: 4
- Validation status: passed
- A4 portrait pages: yes
- Link annotations to note PDFs: 10
- Missing expected titles, filenames, page counts, or collection totals: 0
- Blank pages: 0
- Page-number footer issues: 0
- Formatting issue detected: the first index render placed the day label too close to the day number.
- Formatting adjustment applied: repositioned the day label and number, re-rendered all index pages, and confirmed clean separation.
- Visual style: adapted from `DSA-Design/output/pdf/Day-00-Foundation-Learning-Index.pdf` using the actual collection titles, groups, filenames, and page counts.

## Validation checks performed

- Reopened every PDF with `pypdf` and `pdfplumber` and confirmed every file was readable and nonempty.
- Confirmed all note pages are A4 portrait and all body text stays inside the 18 mm margins; page numbers are the only note footers.
- Compared every visible rendered text fragment with extracted PDF text after whitespace-only layout normalization; coverage was 100% for every note.
- Confirmed source heading order, fenced-block counts, table counts, filenames, and special characters.
- Confirmed every detected LaTeX expression is typeset and no raw LaTeX command from those expressions remains visible.
- Confirmed there are no Mermaid blocks in the source set, so Mermaid rendering mode, diagram orientation, and visual reflow are not applicable.
- Raster-rendered all 661 final note pages at 36 DPI for blank-page and printable-boundary checks; high-resolution representative pages were also visually inspected.
- Recomputed every source SHA-256 checksum after generation and validation; all checksums match the pre-generation inventory.

## Final status

All 10 note PDFs and the index PDF validated successfully. All original Markdown files remained unchanged. No unresolved rendering issues remain.
