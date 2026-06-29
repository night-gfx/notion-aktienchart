# Fix: Zeitraum-Buttons

Replace only `index.html`.

The earlier version used `setVisibleRange()` to shift the time axis. In some
embeds this did not visibly change the chart.

This version filters the daily observations before plotting:
- 1J = only data from the last 1 year
- 3J = only data from the last 3 years
- 5J = only data from the last 5 years
- 10J = only data from the last 10 years
- 20J = only data from the last 20 years
- Alles = complete available history

For `Indexiert 100`, every selected series starts at 100 at the beginning of
the currently selected period.
