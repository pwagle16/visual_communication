"""viscomm -- a small charting library with one consistent, accessible look."""

from .core import CATEGORICAL, CHROME, bar, contrast_ink, line, pie, scatter

__version__ = "0.2.0"
__all__ = [
    "bar",
    "line",
    "scatter",
    "pie",
    "CATEGORICAL",
    "CHROME",
    "contrast_ink",
]
