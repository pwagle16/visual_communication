"""Simple plotting helpers.

Each function takes a pandas DataFrame, draws one chart in the chosen visual
``style``, and saves it to a PNG file. They return the path (a plain string).
Same rules as the rest of the library: pandas in, boring names, no classes.

Chart types: plot_missing, plot_histogram, plot_numeric (bars/histograms),
plot_scatter, plot_line, plot_correlation.
Available styles: "light" (default), "dark", "minimal", "bold".
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # write image files without needing a display
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from simple_eda import styles  # noqa: E402
from simple_eda.core import _check_dataframe, numeric_columns  # noqa: E402


def _finish(fig, ax, style: dict, title: str, path: str) -> str:
    ax.set_title(title, color=style["ink"], fontweight=style["title_weight"])
    styles.apply(ax, fig, style)
    fig.tight_layout()
    fig.savefig(path, dpi=120, facecolor=style["surface"])
    plt.close(fig)
    return path


def _label_bars(ax, bars, style: dict) -> None:
    # Direct value labels: the "relief" that keeps identity/magnitude readable
    # even when a fill sits below the 3:1 contrast line.
    for bar in bars:
        height = bar.get_height()
        text = f"{height:.0f}" if float(height).is_integer() else f"{height:.1f}"
        ax.annotate(
            text,
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            color=style["ink"],
            fontsize=9,
        )


def plot_missing(df: pd.DataFrame, path: str = "missing.png", style: str = "light") -> str:
    """Bar chart of the number of missing values in each column."""
    _check_dataframe(df)
    st = styles.get_style(style)
    counts = df.isna().sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        counts.index, counts.values,
        color=[styles.color(st, i) for i in range(len(counts))],
        edgecolor=st["bar_edge"], linewidth=1.5,
    )
    _label_bars(ax, bars, st)
    ax.set_ylabel("missing count")
    return _finish(fig, ax, st, "Missing values per column", path)


def plot_histogram(df: pd.DataFrame, column: str, path: str = "histogram.png",
                   style: str = "light") -> str:
    """Histogram of a single numeric column."""
    _check_dataframe(df)
    if column not in df.columns:
        raise KeyError(f"no column named {column!r}")
    st = styles.get_style(style)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df[column].dropna(), bins=10, color=styles.color(st, 0),
            edgecolor=st["bar_edge"])
    ax.set_xlabel(column)
    ax.set_ylabel("count")
    return _finish(fig, ax, st, f"Distribution of {column}", path)


def plot_numeric(df: pd.DataFrame, path: str = "numeric.png", style: str = "light") -> str:
    """One histogram per numeric column, laid out in a row."""
    _check_dataframe(df)
    st = styles.get_style(style)
    cols = numeric_columns(df)
    if not cols:
        raise ValueError("no numeric columns to plot")
    fig, axes = plt.subplots(1, len(cols), figsize=(4 * len(cols), 4))
    if len(cols) == 1:
        axes = [axes]
    for i, (ax, col) in enumerate(zip(axes, cols)):
        ax.hist(df[col].dropna(), bins=10, color=styles.color(st, i),
                edgecolor=st["bar_edge"])
        ax.set_title(col, color=st["ink"], fontweight=st["title_weight"])
        styles.apply(ax, fig, st)
    fig.suptitle("Numeric columns", color=st["ink"], fontweight=st["title_weight"])
    fig.set_facecolor(st["surface"])
    fig.tight_layout()
    fig.savefig(path, dpi=120, facecolor=st["surface"])
    plt.close(fig)
    return path


def _need_column(df, name):
    if name not in df.columns:
        raise KeyError(f"no column named {name!r}")


def plot_scatter(df: pd.DataFrame, x: str, y: str, path: str = "scatter.png",
                 style: str = "light") -> str:
    """Scatter plot of two columns, x against y."""
    _check_dataframe(df)
    _need_column(df, x)
    _need_column(df, y)
    st = styles.get_style(style)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df[x], df[y], s=60, color=styles.color(st, 0),
               edgecolor=st["bar_edge"], linewidth=0.8, alpha=0.9)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return _finish(fig, ax, st, f"{y} vs {x}", path)


def plot_line(df: pd.DataFrame, x: str, y, path: str = "line.png",
              style: str = "light") -> str:
    """Line chart of one or more y columns against x.

    ``y`` may be a single column name or a list of names (one line each).
    """
    _check_dataframe(df)
    _need_column(df, x)
    columns = [y] if isinstance(y, str) else list(y)
    st = styles.get_style(style)
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, col in enumerate(columns):
        _need_column(df, col)
        ax.plot(df[x], df[col], marker="o", linewidth=2,
                color=styles.color(st, i), label=col)
    ax.set_xlabel(x)
    if len(columns) > 1:
        ax.legend(frameon=False, labelcolor=st["ink"])
    title = columns[0] if len(columns) == 1 else "trends"
    return _finish(fig, ax, st, f"{title} over {x}", path)


def plot_bar(df: pd.DataFrame, category: str, value: str, group: str = None,
             path: str = "bar.png", style: str = "light", agg: str = "mean") -> str:
    """Bar chart of an aggregated ``value`` per ``category``.

    ``agg`` is any pandas aggregation ("mean", "sum", "median", ...).
    Pass ``group`` to split each category into side-by-side bars (one per
    level of the grouping column) — e.g. treatment split by diet.
    """
    _check_dataframe(df)
    _need_column(df, category)
    _need_column(df, value)
    st = styles.get_style(style)
    fig, ax = plt.subplots(figsize=(7, 4.5))

    if group is None:
        # One measure across categories -> a single hue, sorted for ranking.
        means = df.groupby(category)[value].agg(agg).sort_values(ascending=False)
        bars = ax.bar(means.index.astype(str), means.values,
                      color=styles.color(st, 0), edgecolor=st["bar_edge"], linewidth=1.5)
        _label_bars(ax, bars, st)
    else:
        # Each group level is its own series -> categorical hues + a legend.
        _need_column(df, group)
        table = df.groupby([category, group])[value].agg(agg).unstack(group)
        cats = list(table.index.astype(str))
        levels = list(table.columns)
        width = 0.8 / len(levels)
        x = range(len(cats))
        for gi, level in enumerate(levels):
            offset = [xi + (gi - (len(levels) - 1) / 2) * width for xi in x]
            ax.bar(offset, table[level].values, width=width * 0.92,
                   color=styles.color(st, gi), edgecolor=st["bar_edge"],
                   linewidth=1.2, label=str(level))
        ax.set_xticks(list(x), cats)
        ax.legend(title=group, frameon=False, labelcolor=st["ink"])

    ax.set_ylabel(f"{agg} {value}")
    return _finish(fig, ax, st, f"{agg} {value} by {category}", path)


def plot_box(df: pd.DataFrame, category: str, value: str, path: str = "box.png",
             style: str = "light") -> str:
    """Box plot of ``value`` for each level of ``category``.

    Shows the median, spread, and outliers per group — good for comparing
    how consistent each treatment is, not just its average.
    """
    _check_dataframe(df)
    _need_column(df, category)
    _need_column(df, value)
    st = styles.get_style(style)
    groups = list(df[category].dropna().unique())
    data = [df.loc[df[category] == g, value].dropna().values for g in groups]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bp = ax.boxplot(data, tick_labels=[str(g) for g in groups], patch_artist=True,
                    medianprops={"color": st["ink"], "linewidth": 2})
    for i, box in enumerate(bp["boxes"]):
        box.set(facecolor=styles.color(st, i), edgecolor=st["bar_edge"], alpha=0.9)
    for part in ("whiskers", "caps"):
        for line in bp[part]:
            line.set_color(st["muted"])
    ax.set_ylabel(value)
    return _finish(fig, ax, st, f"{value} by {category}", path)


def plot_correlation(df: pd.DataFrame, path: str = "correlation.png",
                     style: str = "light") -> str:
    """Heatmap of correlations between the numeric columns."""
    _check_dataframe(df)
    cols = numeric_columns(df)
    if len(cols) < 2:
        raise ValueError("need at least two numeric columns for a correlation heatmap")
    st = styles.get_style(style)
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(1.2 * len(cols) + 2, 1.2 * len(cols) + 1))
    im = ax.imshow(corr.values, cmap="Blues", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)), cols, rotation=45, ha="right")
    ax.set_yticks(range(len(cols)), cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                    color="white" if abs(corr.values[i, j]) > 0.5 else st["ink"])
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Correlation", color=st["ink"], fontweight=st["title_weight"])
    fig.set_facecolor(st["surface"])
    ax.set_facecolor(st["surface"])
    ax.tick_params(colors=st["muted"])
    fig.tight_layout()
    fig.savefig(path, dpi=120, facecolor=st["surface"])
    plt.close(fig)
    return path
