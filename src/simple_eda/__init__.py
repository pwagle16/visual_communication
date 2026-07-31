"""simple_eda: the simplest possible exploratory-data-analysis helpers.

    import simple_eda as eda

    # text summaries (plain objects out)
    eda.summarize(df)         # {"rows": ..., "columns": ..., "names": [...]}
    eda.missing(df)           # pandas Series of missing counts per column
    eda.numeric_columns(df)   # list of numeric column names

    # visuals (each saves a PNG and returns its path)
    eda.plot_missing(df)      # bar chart of missing values
    eda.plot_histogram(df, "age")  # one numeric column
    eda.plot_numeric(df)      # a histogram per numeric column
"""

from simple_eda.core import missing, numeric_columns, summarize
from simple_eda.plots import plot_histogram, plot_missing, plot_numeric

__version__ = "0.2.0"
__all__ = [
    "summarize",
    "missing",
    "numeric_columns",
    "plot_missing",
    "plot_histogram",
    "plot_numeric",
]
