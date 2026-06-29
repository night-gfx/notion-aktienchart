# Fix: visible X-axis range

Replace only `index.html`.

## What was wrong
The previous versions either filtered data or used a date-based viewport that
could be overridden by the final iframe layout. Therefore the y-axis changed
but the initial x-axis view sometimes stayed unchanged.

## What this version does
- all daily history is always loaded into Lightweight Charts™
- `1J / 3J / 5J / 10J / 20J` uses `setVisibleLogicalRange()`
- `Alles` uses `fitContent()`
- the range is applied after two animation frames and again after 120 ms,
  which is important inside a GitHub Pages / Notion iframe
- the user can still drag left after a period is selected; that is deliberate,
  because full history remains accessible
- the button **Nur Energy** is removed

In the status, `X-Achse: Zeitfenster gesetzt` confirms that a specific range
was applied.
