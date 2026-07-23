# viscomm

A small, opinionated Python charting library. Four core chart types --
bar, line, scatter, pie -- built on matplotlib, with an accessible,
validated color system and consistent styling baked in so you don't have
to hand-tune each chart.

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

Every chart function returns a standard matplotlib `Axes`, so you can keep
customizing with plain matplotlib calls, or lay several charts out with
`ax.figure` / `plt.subplots` as usual.

Run `examples/basic_usage.py` to generate a sample PNG for each chart type.

## Design principles

The styling follows a fixed procedure rather than per-chart taste calls:

- **One axis.** No chart function offers a second y-axis. Two measures of
  different scale should be two charts, small multiples, or indexed to a
  common base -- not a dual-axis chart.
- **Categorical color is assigned in a fixed order, never cycled.** Series
  get colors by position (`viscomm.theme.CATEGORICAL`), in the order you
  pass them. The order is validated for colorblind-safe adjacent-pair
  contrast (worst-case ΔE 9.1 light / 8.4 dark, OKLab). `bar()` and
  `line()` support up to 8 series on that basis.
- **Scatter is capped at 3 groups.** A scatter plot shows every pair of
  groups on screen at once, so it needs *all-pairs* validation, not just
  adjacent-pair -- only the first 3 palette slots clear that stricter bar.
  Beyond that, fold extra groups into "Other" or facet into small
  multiples rather than adding a 4th color.
- **A legend is always present for 2+ series, never for 1.** With one
  series there's only one color, so the title already says what's
  plotted; a one-swatch legend box just restates it.
- **Fixed mark specs, not per-chart choices**: 2px lines, round joins;
  markers >= 8px with a surface-color ring so they stay legible over a
  line; bars capped at 60% of their slot so neighbors keep visible air
  between them; hairline (1px) gridlines a step off the surface color,
  never dashed.
- **Text never wears the series color.** Axis labels, ticks, and legend
  text use fixed ink tokens (primary/secondary/muted); identity comes from
  the colored mark next to the text, never from coloring the text itself.
  The one exception is a pie chart's in-wedge percentage label, which
  switches between white and dark ink per-wedge so it always has
  contrast against that wedge's fill.

To re-theme, edit the values in `src/viscomm/theme.py`
(`CATEGORICAL`, `CHROME`, `MARK`) -- the chart functions consume them by
role, so nothing else needs to change. If you swap in your own colors,
re-validate the categorical order for colorblind-safe adjacent pairs
before shipping it.

## Known limitations (v1)

- Bars render as plain rectangles (no rounded data-end) -- matplotlib
  doesn't do this natively without custom patches; a reasonable follow-up
  if it matters for your use case.
- No built-in dark mode; `CHROME` currently assumes a light surface.
- Static output only (PNG/SVG/etc. via matplotlib) -- no interactive
  hover/tooltip layer.
