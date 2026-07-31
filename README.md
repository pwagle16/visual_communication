# simple_eda

The simplest possible exploratory-data-analysis helpers for pandas DataFrames.

- **Simple API** — flat, top-level functions. No classes to learn.
- **Boring names** — `summarize`, `missing`, `numeric_columns`, `plot_missing`, ...
- **Pandas in, plain objects out** — dicts, lists, ints, strings, pandas Series, and PNG chart files.

## Install

```bash
pip install -e .
```

## Usage

```python
import pandas as pd
import simple_eda as eda

df = pd.DataFrame({
    "name": ["Ana", "Bo", None],
    "age": [25, None, 31],
})

print(eda.summarize(df))
# {'rows': 3, 'columns': 2, 'names': ['name', 'age']}

print(eda.numeric_columns(df))
# ['age']

print(eda.missing(df))
# name    1
# age     1
# dtype: int64
```

### Charts

Each plotting function draws one chart, saves it to a PNG, and returns the path:

```python
eda.plot_missing(df, "missing.png")               # bar chart of missing values
eda.plot_histogram(df, "age", "age.png")          # histogram of one column
eda.plot_numeric(df, "numeric.png")               # a histogram per numeric column
eda.plot_scatter(df, "ad_spend", "revenue", "scatter.png")   # scatter of two columns
eda.plot_line(df, "month", ["revenue", "ad_spend"], "line.png")  # line chart
eda.plot_bar(df, "treatment", "reduction", path="bar.png")       # aggregated bar
eda.plot_bar(df, "treatment", "reduction", group="diet", path="grouped.png")  # grouped bar
eda.plot_box(df, "treatment", "reduction", "box.png")            # box plot per group
eda.plot_correlation(df, "corr.png")              # correlation heatmap
```

There's a worked hospital example in `examples/cholesterol_trial.py` (run
`examples/generate_trial_data.py` first) that compares three cholesterol pills
against a placebo and shows the effect of exercise and a fat-free diet.

### Visual styles

Every plotting function takes a `style` argument. The colors are colorblind-safe
(validated with a palette checker) and bars carry direct value labels.

```python
eda.plot_missing(df, "missing.png", style="dark")
eda.STYLES   # ['light', 'dark', 'minimal', 'bold']
```

| Style | Look |
| --- | --- |
| `light` *(default)* | white surface, soft grid, full palette |
| `dark` | dark surface, hues re-stepped for it |
| `minimal` | single blue, no grid, no top/right spines |
| `bold` | high-contrast, heavy titles, hard edges |

Or run it against the bundled dataset:

```bash
python examples/basic_usage.py
```

## API

| Function | Returns | Description |
| --- | --- | --- |
| `summarize(df)` | `dict` | `rows`, `columns`, and column `names`. |
| `missing(df)` | `pandas.Series` | Count of missing values per column. |
| `numeric_columns(df)` | `list` | Names of the numeric columns. |
| `plot_missing(df, path)` | `str` | Bar chart of missing values → PNG path. |
| `plot_histogram(df, column, path)` | `str` | Histogram of one column → PNG path. |
| `plot_numeric(df, path)` | `str` | A histogram per numeric column → PNG path. |
| `plot_scatter(df, x, y, path)` | `str` | Scatter of two columns → PNG path. |
| `plot_line(df, x, y, path)` | `str` | Line chart (`y` = name or list) → PNG path. |
| `plot_bar(df, category, value, group=None, path)` | `str` | Aggregated bar per category, optional grouping → PNG path. |
| `plot_box(df, category, value, path)` | `str` | Box plot of `value` per group → PNG path. |
| `plot_correlation(df, path)` | `str` | Correlation heatmap → PNG path. |

Every function accepts a pandas `DataFrame` and raises `TypeError` on anything else.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
