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
- the analysis charts use the average of the minimum and maximum forward return within each selected horizon
- the upper-right price/return chart marks each selected commodity's current price with an interactive vertical reference
- both show fixed 1, 3, 6, 12, and 24-month horizons with consistent horizon colors
- clicking, tapping, or keyboard-activating a horizon legend toggles it in both right-hand charts
- at least one forward horizon always remains visible
- a responsive 2-column × 3-row layout provides six panel positions for price, indicator, and forward-return analysis
- indicator lookback can be entered freely in months
- absolute momentum is `current price - lookback price`
- absolute momentum is min-max scaled from 0 to 1 using only observations available up to each historical date
- the variable momentum weight `alpha` accepts values from 0 through 1 in 0.05 steps
- the final indicator is `((1 - alpha) + alpha × scaled momentum) / current price`; `alpha = 1` is full momentum and `alpha = 0` reduces the formula to `1 / price`
- when `Log-Performance` is selected, price-based analysis values and momentum differences use `q = ln(price)` where applicable
- in log mode, momentum is `ln(current price) - ln(lookback price)`, then min-max scaled and divided by the actual current price
- the forward target is `0.5 × (((minimum future price / current price) - 1) + ((maximum future price / current price) - 1)) × 100`, including in log mode
- normal price and Index 100 modes keep the existing normal-price analysis calculations
- the lower-left D3 chart overlays the indicator and actual price as interactive time series
- hover or click selects a date and shows both the indicator and price; current points are marked
- the middle-right D3 scatter plot compares the currently selected momentum/price lookback with the five average min/max forward returns
- changing the indicator lookback or alpha updates the momentum time series, both indicator/model charts, and the fixed train/test backtest
- the bottom-left panel shows the first configurable 3 through 24 years as in-sample observations in the same indicator/return scatter-plot style
- only returns fully known by the training cutoff are admitted to the in-sample fit; later observation dates are out-of-sample
- the bottom-right panel compares predicted and actual 12M/24M average min/max forward returns using models fitted once on the in-sample window
- both lower chart titles show their exact in-sample or out-of-sample date range
- linear regression is excluded from the bottom train/test model selection; logarithmic, exponential, power, quadratic, cubic, and fourth-degree polynomial candidates remain
- the out-of-sample summary shows R-squared, RMSE, and the mean actual versus mean predicted return to make regression-to-the-mean visible
- the price/return and indicator/return charts automatically select the best tested equation for 12M and 24M only (linear, logarithmic, exponential, power, or quadratic) using a chronological holdout test
- the selected 12M and 24M equations, model names, and test R-squared values are shown above the charts; 1M, 3M, and 6M remain point series without fitted curves
- a third two-column row expands the dashboard to six panel positions; its left position is intentionally empty
- a vertical reference marks the current indicator; its future returns are explicitly shown as unknown
- the momentum lookback input accepts 0.2-month steps from 0.2 through 24 months
