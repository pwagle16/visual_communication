"""Simple plotting helpers.

Each function takes a pandas DataFrame, draws one chart, and saves it to a
PNG file. They return the path (a string) so the result stays a plain object.
Same rules as the rest of the library: pandas in, boring names, no classes.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # write image files without needing a display
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from simple_eda.core import _check_dataframe, numeric_columns  # noqa: E402


def _save(fig, path: str) -> str:
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_missing(df: pd.DataFrame, path: str = "missing.png") -> str:
    """Bar chart of the number of missing values in each column."""
    _check_dataframe(df)
    counts = df.isna().sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values, color="#d9534f")
    ax.set_title("Missing values per column")
    ax.set_ylabel("missing count")
    return _save(fig, path)


def plot_histogram(df: pd.DataFrame, column: str, path: str = "histogram.png") -> str:
    """Histogram of a single numeric column."""
    _check_dataframe(df)
    if column not in df.columns:
        raise KeyError(f"no column named {column!r}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df[column].dropna(), bins=10, color="#5b9bd5", edgecolor="white")
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("count")
    return _save(fig, path)


def plot_numeric(df: pd.DataFrame, path: str = "numeric.png") -> str:
    """One histogram per numeric column, laid out in a grid."""
    _check_dataframe(df)
    cols = numeric_columns(df)
    if not cols:
        raise ValueError("no numeric columns to plot")
    fig, axes = plt.subplots(1, len(cols), figsize=(4 * len(cols), 4))
    if len(cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        ax.hist(df[col].dropna(), bins=10, color="#5b9bd5", edgecolor="white")
        ax.set_title(col)
    fig.suptitle("Numeric columns")
    return _save(fig, path)
