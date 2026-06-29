# Update: tägliche Daten, weißer Hintergrund, Linienform

This update replaces only two existing files:

```text
index.html
scripts/update_commodities.py
```

After both files are committed, GitHub automatically starts the existing
workflow **Update data and deploy dashboard**. That workflow overwrites
`data/commodities.json` with daily close prices and redeploys the website.

Changes:
- **Linienform** select: `Normal` or `Geglättet / kurvig`
- no horizontal or vertical grid lines
- pure white chart backdrop
- daily historical closing prices instead of weekly observations
