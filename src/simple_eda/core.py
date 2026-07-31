"""Core exploratory-data-analysis helpers.

Every function takes a pandas DataFrame and returns plain Python objects
(dicts, lists, ints, strings) or a pandas Series. No custom classes.
"""

from __future__ import annotations

import pandas as pd


def _check_dataframe(df: object) -> None:
    """Raise a clear error if ``df`` is not a pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"expected a pandas DataFrame, got {type(df).__name__}"
        )


def summarize(df: pd.DataFrame) -> dict:
    """Return the shape and column names of ``df``.

    >>> import pandas as pd
    >>> summarize(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    {'rows': 2, 'columns': 2, 'names': ['a', 'b']}
    """
    _check_dataframe(df)
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "names": list(df.columns),
    }


def missing(df: pd.DataFrame) -> pd.Series:
    """Return the number of missing values in each column.

    The result is a pandas Series indexed by column name.
    """
    _check_dataframe(df)
    return df.isna().sum()


def numeric_columns(df: pd.DataFrame) -> list:
    """Return the names of the numeric columns in ``df``."""
    _check_dataframe(df)
    return list(df.select_dtypes(include="number").columns)
