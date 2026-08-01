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

Straight from GitHub:

```bash
pip install "git+https://github.com/pwagle16/visual_communication.git@main"
```

Or, if you've cloned the repo, an editable install from inside it:

```bash
pip install -e ".[dev]"
```

## Usage

```python
import viscomm as vc
import matplotlib.pyplot as plt

vc.bar(
    ["Q1", "Q2", "Q3", "Q4"],
    series={"2024": [12, 18, 14, 22], "2025": [15, 20, 19, 27]},
    title="Quarterly revenue",
    subtitle="$ millions",
    ylabel="$M",
)
plt.show()          # pop the chart open in a window
```

Every chart function takes either a single series (`values=` / `y=`) or a
`series={name: data}` dict for multiple series, and returns a standard
matplotlib `Axes`. That means you can save it, keep customizing with plain
matplotlib, or lay several charts out on one figure by passing `ax=` from
`plt.subplots`:

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
vc.line(range(2019, 2026), series={"North": [10, 12, 15, 14, 18, 22, 25]}, ax=axes[0])
vc.pie(["Direct", "Organic", "Referral", "Paid"], [35, 30, 20, 15], ax=axes[1])
fig.savefig("dashboard.png", dpi=150)
```

> When a chart makes its own figure it gets the coffee beans automatically.
> When you compose several charts onto one shared figure with `ax=`, the
> beans are skipped so the dashboard stays clean.

## API

| Function | Single series | Multiple series |
|---|---|---|
| `vc.bar(categories, values=...)` | `values=[...]` | `series={name: [...]}` (grouped), `horizontal=True` |
| `vc.line(x, y=...)` | `y=[...]` | `series={name: [...]}` |
| `vc.scatter(x, y=...)` | `x=[...], y=[...]` | `series={name: (xs, ys)}` (max 3) |
| `vc.pie(labels, values)` | — | — |

All four accept `title`, `subtitle`, `ax`, and `figsize`; the axis charts
also accept `xlabel` / `ylabel`. `bar()` and `line()` also accept `colors=`
to override the coffee palette.

## Design principles

The styling follows a fixed procedure rather than per-chart taste calls:

- **Coffee by default.** The palette is a set of coffee browns (espresso
  first, so the leading series stands out), the surface is a warm latte
  cream, and roasted coffee beans are drawn into the four corners of every
  chart the library owns -- aspect-corrected so they stay bean-shaped and
  placed clear of the title, legend, and axis labels.
- **One axis.** No chart function offers a second y-axis. Two measures of
  different scale should be two charts, small multiples, or indexed to a
  common base -- not a dual-axis chart.
- **Categorical color is assigned in a fixed order, never cycled.** Series
  get colors by position (`viscomm.CATEGORICAL`), in the order you pass
  them. `bar()` and `line()` support up to 8 series.
- **Scatter is capped at 3 groups.** A scatter plot shows every pair of
  groups on screen at once, so adjacent points get hard to tell apart by
  color beyond three -- fold extra groups into "Other" or facet into small
  multiples.
- **A legend is always present for 2+ series, never for 1.** With one
  series there's only one color, so the title already says what's plotted.
- **Fixed mark specs, not per-chart choices**: 2px lines with round joins;
  markers with a surface-color ring so they stay legible over a line; a
  cluster of grouped bars fills 80% of its category slot with a thin
  surface-color gap between adjacent bars; hairline gridlines a step off the
  surface color, never dashed.
- **Text never wears the series color.** Axis labels, ticks, and legend
  text use fixed ink tokens; the one exception is a pie chart's in-wedge
  percentage label, which switches between white and dark ink per-wedge
  (`contrast_ink`) so it always has contrast against its fill.

To re-theme, edit `CATEGORICAL` and `CHROME` at the top of
`src/viscomm/core.py` (and `_BEAN_ROASTS` / `_BEAN_SPOTS` for the beans) --
the chart functions consume them by role, so nothing else needs to change.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Known limitations

- No built-in dark mode; `CHROME` assumes a light latte surface.
- Static output only (PNG/SVG/etc. via matplotlib) -- no interactive
  hover/tooltip layer.
