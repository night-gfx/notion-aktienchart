# Clean start: Rohstoffvergleich mit Lightweight Charts™

## This package contains

```text
index.html
requirements.txt
data/commodities.json
scripts/update_commodities.py
.github/workflows/update-and-deploy.yml
```

- **index.html**: Your GitHub Pages / Notion dashboard.
- **Lightweight Charts™**: Draws all lines in fixed, different colors.
- **data/commodities.json**: Created by the workflow; it starts empty.
- **Python updater**: Downloads Yahoo Finance history via yfinance.
- **One GitHub workflow**: Downloads data, updates the JSON file, and deploys the site.

## Important Pages setting

Use **GitHub Actions** as the GitHub Pages source — not "Deploy from a branch".

## First run

Open **Actions** → **Update data and deploy dashboard** → **Run workflow**.

Wait until both jobs — `build` and `deploy` — show green check marks. Then open:

```text
https://night-gfx.github.io/notion-aktienchart/?version=10
```

## If a page is blank

1. Open the browser URL directly, not Notion.
2. Go to **Actions** and open the most recent failed job.
3. Read the red error text under the failed step. The usual causes are:
   - GitHub Pages source still set to "Deploy from a branch".
   - Workflow permissions are still read-only.
   - Not all files/folders from the ZIP were uploaded.

The workflow uses `contents: write`, `pages: write`, and `id-token: write`.
If your repository settings override this, set:
**Settings → Actions → General → Workflow permissions → Read and write permissions**.
