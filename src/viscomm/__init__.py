from .bar import bar
from .line import line
from .pie import pie
from .scatter import scatter
from .theme import (
    CATEGORICAL,
    CHROME,
    THEMES,
    active_theme,
    palette,
    set_theme,
)

__version__ = "0.1.0"
__all__ = [
    "bar",
    "line",
    "scatter",
    "pie",
    "set_theme",
    "active_theme",
    "palette",
    "THEMES",
    "CATEGORICAL",
    "CHROME",
]
