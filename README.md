# viscomm

A small, opinionated, **coffee-themed** Python charting library. Four core
chart types -- bar, line, scatter, pie -- built on matplotlib. Every chart
comes out in a warm brown, latte-cream look with roasted coffee beans tucked
into the corners **automatically, whatever data you give it** -- no styling
required on your end. The whole library is a single module
(`src/viscomm/core.py`).

```python
import viscomm as vc
vc.bar(["A", "B", "C"], values=[3, 7, 5], title="Sales")   # already brown + beans
```

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```python
import viscomm as vc

ax = vc.bar(
    ["Q1", "Q2", "Q3", "Q4"],
    series={"2024": [12, 18, 14, 22], "2025": [15, 20, 19, 27]},
    title="Quarterly revenue",
    subtitle="$ millions",
    ylabel="$M",
)
ax.figure.savefig("revenue.png", dpi=150)
```

Every chart function takes either a single series (`values=` / `y=`) or a
`series={name: data}` dict for multiple series, and returns a standard
matplotlib `Axes` -- so you can keep customizing with plain matplotlib, or
lay several charts out on one figure by passing `ax=` from `plt.subplots`.

```python
import matplotlib.pyplot as plt
import viscomm as vc

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
vc.line(range(2019, 2026), series={"North": [10, 12, 15, 14, 18, 22, 25]}, ax=axes[0])
vc.pie(["Direct", "Organic", "Referral", "Paid"], [35, 30, 20, 15], ax=axes[1])
```

Run `examples/basic_usage.py` to generate a sample PNG for each chart type
into `examples/output/`.

## Test dataset

`data/coffee_sales.csv` is a small, tidy sample dataset (48 rows: 12 months
× 4 regions, columns `month, region, revenue_k, orders, ad_spend_k`) rich
enough to drive every chart type. Regenerate it any time with
`python examples/generate_data.py` (deterministic — fixed seed).

`examples/from_csv.py` loads it with the standard-library `csv` module and
renders two charts side by side (`examples/output/coffee_sales.png`):
monthly revenue lines per region and a total-revenue bar chart. It uses a
soft brown pastel palette via the `colors=` argument, with the
highest-revenue region drawn in dark brown; colors are mapped per region so
each region keeps the same color in both charts. `pandas.read_csv` works
too — viscomm takes plain lists either way.

Both `bar()` and `line()` accept `colors=` to override the default palette
(one color per series, or one per bar for a single-series bar chart).

## API

| Function | Single series | Multiple series |
|---|---|---|
| `vc.bar(categories, values=...)` | `values=[...]` | `series={name: [...]}` (grouped), `horizontal=True` |
| `vc.line(x, y=...)` | `y=[...]` | `series={name: [...]}` |
| `vc.scatter(x, y=...)` | `x=[...], y=[...]` | `series={name: (xs, ys)}` (max 3) |
| `vc.pie(labels, values)` | — | — |

All four accept `title`, `subtitle`, `ax`, and `figsize`; the axis charts
also accept `xlabel` / `ylabel`.

## Design principles

The styling follows a fixed procedure rather than per-chart taste calls:

- **One axis.** No chart function offers a second y-axis. Two measures of
  different scale should be two charts, small multiples, or indexed to a
  common base -- not a dual-axis chart.
- **Categorical color is assigned in a fixed order, never cycled.** Series
  get colors by position (`viscomm.CATEGORICAL`), in the order you pass
  them. The order is validated for colorblind-safe adjacent-pair contrast.
  `bar()` and `line()` support up to 8 series on that basis.
- **Scatter is capped at 3 groups.** A scatter plot shows every pair of
  groups on screen at once, so it needs *all-pairs* separation, not just
  adjacent-pair -- only the first 3 palette slots clear that stricter bar.
  Beyond that, fold extra groups into "Other" or facet into small multiples.
- **A legend is always present for 2+ series, never for 1.** With one
  series there's only one color, so the title already says what's plotted;
  a one-swatch legend box just restates it.
- **Fixed mark specs, not per-chart choices**: 2px lines with round joins;
  markers with a surface-color ring so they stay legible over a line; a
  cluster of grouped bars fills 80% of its category slot with a thin
  surface-color gap between adjacent bars (touching marks are separated by
  a gap, never a drawn border); hairline gridlines a step off the surface
  color, never dashed.
- **Text never wears the series color.** Axis labels, ticks, and legend
  text use fixed ink tokens (primary/secondary/muted); identity comes from
  the colored mark next to the text. The one exception is a pie chart's
  in-wedge percentage label, which switches between white and dark ink
  per-wedge (`contrast_ink`) so it always has contrast against its fill.

To re-theme, edit `CATEGORICAL` and `CHROME` at the top of
`src/viscomm/core.py` -- the chart functions consume them by role, so
nothing else needs to change. If you swap in your own colors, re-validate
the categorical order for colorblind-safe adjacent pairs before shipping.

## Known limitations

- No built-in dark mode; `CHROME` currently assumes a light surface.
- Static output only (PNG/SVG/etc. via matplotlib) -- no interactive
  hover/tooltip layer.
