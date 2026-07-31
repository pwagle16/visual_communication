"""simple_eda: the simplest possible exploratory-data-analysis helpers.

    import simple_eda as eda

    eda.summarize(df)   # {"rows": ..., "columns": ..., "names": [...]}
    eda.missing(df)     # pandas Series of missing counts per column
    eda.numeric_columns(df)  # list of numeric column names
"""

from simple_eda.core import missing, numeric_columns, summarize

__version__ = "0.1.0"
__all__ = ["summarize", "missing", "numeric_columns"]
