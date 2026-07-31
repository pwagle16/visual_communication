"""simple_eda: the simplest possible exploratory-data-analysis helpers.

    import simple_eda as eda

    # text summaries (plain objects out)
    eda.summarize(df)         # {"rows": ..., "columns": ..., "names": [...]}
    eda.missing(df)           # pandas Series of missing counts per column
    eda.numeric_columns(df)   # list of numeric column names

    # visuals — many chart types, each saves a PNG and returns its path
    eda.plot_missing(df)                    # bar chart of missing values
    eda.plot_histogram(df, "age")          # histogram of one column
    eda.plot_numeric(df)                    # a histogram per numeric column
    eda.plot_scatter(df, "ad_spend", "revenue")   # scatter of two columns
    eda.plot_line(df, "month", "revenue")         # line chart over an axis
    eda.plot_correlation(df)               # correlation heatmap

    # pick a visual style: "light" (default), "dark", "minimal", "bold"
    eda.plot_scatter(df, "ad_spend", "revenue", style="dark")
    eda.STYLES                              # the available style names
"""

from simple_eda.core import missing, numeric_columns, summarize
from simple_eda.plots import (
    plot_correlation,
    plot_histogram,
    plot_line,
    plot_missing,
    plot_numeric,
    plot_scatter,
)
from simple_eda.styles import STYLES

__version__ = "0.4.0"
__all__ = [
    "summarize",
    "missing",
    "numeric_columns",
    "plot_missing",
    "plot_histogram",
    "plot_numeric",
    "plot_scatter",
    "plot_line",
    "plot_correlation",
    "STYLES",
]
