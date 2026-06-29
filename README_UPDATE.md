# Final control update

Replace only `index.html`.

## What this update changes

### 1. Display range
`1J | 3J | 5J | 10J | 20J | Alles`

The selected range filters the data **before** they are passed to Lightweight
Charts™. `fitContent()` therefore must display exactly the selected time
window. The chart no longer relies on a time-scale movement that can be
overwritten in an embedded page.

### 2. Index base
The display range is independent from the index base. In `Index 100` and
`Log-Performance`, use **Indexbasis** to choose:

- start of displayed range
- 1 / 3 / 5 / 10 / 20 years before last available price
- first common selected observation
- your own calendar date

### 3. Log-Performance
It is now:
`100 × ln(price / base price)`

It is **not** a logarithmic price axis. The base is 0.

### 4. Legend
Every legend item shows the newest original price under its name, in the same
color as the corresponding time series.
