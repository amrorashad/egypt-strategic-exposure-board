# CATALYSTIQ — Free Egypt Strategic Exposure Board

Hosted using GitHub Pages; no paid hosting required.

## Upgrade deployment
Upload `index.html`, replacing existing root file. Upload `data/months.json` in the `data` folder. GitHub Pages will redeploy automatically after commits.

## Monthly editions
Add a source-verified entry to `data/months.json` under `snapshots`. Only confirmed historical editions; never fabricate missing months. Required fields: `id`, `month` (YYYY-MM), `period` (`interim`/`complete`), `label`, `as_of` (YYYY-MM-DD), `reference_baseline` (`CIQ-GEO-2026-10-14`), `indicators` with domains `direct`, `gaza`, `economic`, `maritime`, `diplomatic` and status/observation each, `numeric_metrics` and `sources` source URLs. A new snapshot automatically becomes a selectable archived edition and extends the categorical charts; never use made-up risk scores.

## Important limitations
GitHub Pages is free hosting, **not** automatic verified news research. To publish unattended monthly news requires a trusted source ingestion and verification pipeline plus GitHub repository write access. The current ChatGPT GitHub integration previously returned HTTP 403 for writes, so this upgrade is provided as a manual upload package unless permissions change. The visible verification date prevents old content being presented as current.
