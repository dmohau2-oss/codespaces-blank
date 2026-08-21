---
name: data-processing-workflow
description: "Use when working on this Python CSV data-processing app: diagnose CLI failures, validate or generate input data, run the ETL pipeline, scan outputs, run tests, and optionally publish verified changes to GitHub."
---

# Data Processing Workflow

Use this workflow for requests involving the repository's CSV input, processing pipeline, output files, tests, or GitHub upload.

## 1. Identify The Task

- Treat the user's latest request as authoritative.
- Inspect the current entry point, direct processor path, relevant tests, and Git status before editing.
- State one local hypothesis about the failure or desired behavior and one check that could disconfirm it.
- Preserve unrelated user edits and generated files unless the user explicitly asks to include them.

## 2. Diagnose The CLI

- Run the exact command the user is trying, correcting only obvious shell typos such as `src/ main.py` to `src/main.py`.
- Capture the first actionable exception.
- Inspect the nearest code that directly controls that exception.
- Make the smallest focused fix. Check both supported entry points when relevant:
  - `python src/main.py ...`
  - `python -m src.main ...`

## 3. Validate Input Data

- Confirm the input file exists before processing.
- For this application, the required schema includes `value`; the usual sample columns are `id`, `name`, `value`, and `category`.
- If the requested file is missing, report that clearly. Use the application's documented fallback only when the user accepts fallback behavior.
- When generating rows, create a temporary input file unless the user explicitly requests a repository file.
- Keep numeric values in `value` and preserve category text as data, not code.

## 4. Run Processing

Use the application entry point and an explicit output path, for example:

```bash
python src/main.py --input data/sample_input.csv --output output/processed.csv
```

For grouped results, add `--group-by category`. For JSON exports, use `--summary-json` or `--output-json` as appropriate.

For large datasets:

- Generate exactly the requested row count.
- Include a header and valid required columns.
- Prefer the configured chunked reader; do not replace it with an unbounded custom loader.
- Report row count, total, average, and output paths.

## 5. Scan The Output

Check:

- The output file exists.
- Required columns are present.
- Row count is plausible and matches the processed result.
- Missing-value count is zero unless explicitly expected.
- Duplicate-row count is acceptable.
- Numeric aggregation is consistent with the CLI summary.

## 6. Test

Run the narrowest relevant check first, then the full suite when practical:

```bash
python -m py_compile src/main.py
python -m pytest -q tests/test_processor.py
```

Do not claim success when a test or command exits nonzero. Mention unrelated pre-existing failures separately.

## 7. Publish Carefully

Before publishing:

- Review `git status` and both staged and unstaged diffs.
- Stage only files requested by the user or required by the fix.
- Do not include `.vscode/`, generated output, or unrelated README changes without explicit approval.
- Commit with a concise message only when the user asks to upload or commit.
- Push to the configured remote and report the commit hash.
- A local commit is not an upload. If GitHub returns `403`, report the permission failure and leave the commit intact; do not retry indefinitely or expose credentials.

## Completion Criteria

The workflow is complete only when:

- The requested behavior works or the blocker is explicitly identified.
- Relevant tests pass, or failures are reported.
- Generated outputs and their locations are reported.
- Git status and upload state are accurately described.
