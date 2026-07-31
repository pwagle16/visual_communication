# Demo / video notes

Scratch notes for the walkthrough video. Not shipped as part of the API.

## 1. Install, import, README

```bash
pip install -e .
python examples/basic_usage.py
```

```python
import pandas as pd
import simple_eda as eda
df = pd.read_csv("data/sales.csv")
eda.plot_line(df, "month", ["revenue", "ad_spend"], "line.png")
```

Then show the README's install + usage + API table.

## 2. Two favorite visualizations + the aesthetic choices

**Multi-line trend (`plot_line`).** Each line gets the *next* categorical hue
in a fixed order (blue, then orange) rather than a recycled or random color, so
identity is stable — "blue is always revenue." Lines are 2px with round `o`
markers so individual months stay readable, and the legend is frameless so it
doesn't box in the data. The grid is a faint 20%-opacity gray sitting *below*
the data, present enough to read values off but never competing with the lines.

**Correlation heatmap (`plot_correlation`).** Magnitude is a job for a single
*sequential* hue (blue, light→dark), never a rainbow — darker simply means
"more correlated." Each cell is labeled with its number, and the label flips to
white on the dark cells so text contrast holds either way. That direct labeling
is deliberate: color alone shouldn't carry the value.

Cross-cutting choices: colors come from a colorblind-safe palette that was run
through a validator (not eyeballed); bars carry direct value labels so the chart
is still readable for the few light-mode hues that fall under the 3:1 contrast
line; and text always uses ink colors, never a series hue.

## 3. Two problems and how I resolved them

**Problem 1 — charts couldn't render with no display.** matplotlib defaults to
an interactive backend and blew up in this headless environment. Fixed by
forcing the non-interactive Agg backend (`matplotlib.use("Agg")`) at import in
`plots.py`, so every function writes a PNG instead of opening a window.

**Problem 2 — the library outgrew the 250-line budget.** Adding the four visual
styles pushed the source past 250 lines. Rather than cut features, I collapsed
each style from a ten-line dict literal into a single `_style(...)` constructor
call, which brought it back under budget without losing any styles. (Adding the
new chart types later pushed it over again — a deliberate trade of the line
budget for the scatter/line/heatmap variety that was requested.)

**Problem 3 (bonus) — `pip install build twine` broke on a system package.**
pip tried to upgrade a Debian-managed `packaging` and errored. Resolved by
installing the build tools into the user site (`pip install --user`), leaving
the system package untouched; `python -m build` and `twine check` then passed.
