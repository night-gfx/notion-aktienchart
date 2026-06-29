# Bereinigtes Update

Ersetze ausschließlich `index.html`.

Änderungen:
- Der Button **Nur Energy** wurde entfernt.
- Die Zeitraum-Buttons arbeiten weiterhin als echte Datenfilter:
  `1J | 3J | 5J | 10J | 20J | Alles`.
- Im Status steht zusätzlich:
  `Datei-Historie: [erstes Datum] bis [letztes Datum]`.

## Wichtige Prüfung nach dem Hochladen

1. Wähle **Alles**.
2. Lies den neuen Status.

- Steht dort beispielsweise `Datei-Historie: 1983-... bis 2026-...`,
  aber der Chart startet trotzdem erst 2024, dann ist es ein Chart-/Browserproblem.
- Steht dort `Datei-Historie: 2024-... bis 2026-...`, dann enthält
  `data/commodities.json` selbst keine ältere Historie. Dann müssen wir
  den GitHub-Action-Datenlauf reparieren, nicht die HTML-Datei.
