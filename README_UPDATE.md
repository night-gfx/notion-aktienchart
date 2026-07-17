# Chart-Darstellung

Replace only `index.html`.

## What this version does

- the main time-series chart is rendered as responsive SVG with D3.js
- the price time-series chart uses the same panel header and chart-body layout as the analysis charts
- its heading is simply `Preis`, and the fullscreen button/mode are removed
- `1J / 3J / 5J / 10J / 20J / Alles` filters the displayed data range
- no commodity is selected when the page first opens
- MACD controls, calculations, indicators, and the MACD chart are removed
- the chart provides axes, grid lines, a pointer/touch tooltip, and optional event markers
- current prices are visible in the commodity list and chart legend
- the commodity list also shows the current price percentile over full available history
- the two right-hand analysis charts use ordinary endpoint forward returns rather than maximum returns
- the upper-right price/return chart marks each selected commodity's current price with an interactive vertical reference
- both show fixed 1, 3, 6, 12, and 24-month horizons with consistent horizon colors
- clicking, tapping, or keyboard-activating a horizon legend toggles it in both right-hand charts
- at least one forward horizon always remains visible
- a responsive 2-column × 3-row layout provides six panel positions for price, indicator, and forward-return analysis
- indicator lookback can be entered freely in months
- absolute momentum is `current price - lookback price`
- absolute momentum is min-max scaled from 0 to 1 using only observations available up to each historical date
- the final indicator is `scaled momentum (0–1) / current price`
- when `Log-Performance` is selected, price-based analysis values and momentum differences use `q = ln(price)` where applicable
- in log mode, momentum is `ln(current price) - ln(lookback price)`, then min-max scaled and divided by the actual current price
- the forward-return Y-axes always use the ordinary endpoint return `(future price / current price - 1) × 100`, including in log mode
- normal price and Index 100 modes keep the existing normal-price analysis calculations
- the lower-left D3 chart overlays the indicator and actual price as interactive time series
- hover or click selects a date and shows both the indicator and price; current points are marked
- the middle-right D3 scatter plot compares the fixed 12M momentum/price indicator with the five endpoint forward returns
- the middle-right forward-return analysis uses a fixed 12-month momentum indicator; the lower-left lookback input defaults to 2 months and affects its momentum time series only, while the denominator is always the price at the measurement date
- the price/return and indicator/return charts automatically select the best tested equation for 12M and 24M only (linear, logarithmic, exponential, power, or quadratic) using a chronological holdout test
- the selected 12M and 24M equations, model names, and test R-squared values are shown above the charts; 1M, 3M, and 6M remain point series without fitted curves
- a third two-column row expands the dashboard to six panel positions; its left position is intentionally empty
- the bottom-right control chart fixes momentum at 1, so its indicator is `1 / current price`; comparing its test scores with the 12M momentum chart shows whether momentum improves the approximation
- a vertical reference marks the current indicator; its future returns are explicitly shown as unknown
- the momentum lookback input accepts 0.2-month steps from 0.2 through 24 months
