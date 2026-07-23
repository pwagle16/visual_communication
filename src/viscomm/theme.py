"""Themes (categorical palettes), chrome colors, and mark specs.

The chart functions consume colors by role, never by raw hex, so a theme is
just a list of categorical hues swapped in behind them. Two themes ship:

- "default": the reference palette from the dataviz design method -- an
  eight-hue order validated for colorblind-safe adjacent pairs and contrast.
- "pastel": a soft pink/blue palette. It deliberately does NOT pass the
  accessibility validator (pastels are too light, too low-chroma, and too
  low-contrast); see PALETTE_NOTES below. Pick it for looks, and lean on the
  secondary encoding the library always ships -- a legend for 2+ series,
  surface gaps between bars, markers/end-labels on lines -- to keep it legible.

Select a theme globally with `set_theme("pastel")`, or per chart via the
`theme=` argument every chart function accepts.
"""

# Fixed hue order -- never cycled. Assigned to series by position, in the
# order series are given. Bar/line tolerate all slots (adjacent-pair
# validation); scatter caps at 3 (all-pairs validation) -- see scatter.py.
_DEFAULT = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Soft pink/blue pastels. Ordered to spread the most-similar hues apart, but
# still fails every color check -- kept for aesthetics by explicit choice.
_PASTEL = [
    "#f4a6c6",  # 1 rose pink
    "#a9c9f5",  # 2 powder blue
    "#e3aede",  # 3 orchid
    "#bfe0f2",  # 4 sky blue
    "#f7c5d6",  # 5 blush pink
    "#c7bef0",  # 6 periwinkle
    "#f9cdab",  # 7 peach
    "#a9e6d2",  # 8 mint
]

THEMES = {
    "default": _DEFAULT,
    "pastel": _PASTEL,
}

# What each theme trades away, so callers can make an informed choice.
PALETTE_NOTES = {
    "default": "Passes the dataviz validator: colorblind-safe adjacent pairs "
    "(worst CVD dE 9.1), normal-vision floor clear.",
    "pastel": "NOT accessibility-validated -- fails the lightness band, chroma "
    "floor, CVD separation (worst adjacent dE ~3), and contrast checks. Pastels "
    "on a near-white surface are inherently low-contrast; relies on the "
    "always-on legend, bar gaps, and line markers to stay readable.",
}

_active_theme = "default"


def set_theme(name):
    """Set the active theme used by charts that don't pass an explicit `theme=`."""
    if name not in THEMES:
        raise ValueError(f"unknown theme '{name}'. Available: {', '.join(THEMES)}.")
    global _active_theme
    _active_theme = name


def active_theme():
    """Name of the currently active theme."""
    return _active_theme


def palette(theme=None):
    """Return the categorical hue list for `theme` (or the active theme)."""
    name = theme if theme is not None else _active_theme
    if name not in THEMES:
        raise ValueError(f"unknown theme '{name}'. Available: {', '.join(THEMES)}.")
    return THEMES[name]


# Backwards-compatible alias for the default palette.
CATEGORICAL = _DEFAULT

# Series count where scatter's all-pairs (not just adjacent-pair) CVD
# validation still holds -- see references/palette.md in the dataviz skill.
SCATTER_MAX_SERIES = 3

CHROME = {
    "surface": "#fcfcfb",
    "primary_ink": "#0b0b0b",
    "secondary_ink": "#52514e",
    "muted_ink": "#898781",
    "gridline": "#e1e0d9",
    "baseline": "#c3c2b7",
}

MARK = {
    "line_width": 2.0,
    "marker_size": 8.0,
    "marker_ring_width": 2.0,
    "bar_max_width_frac": 0.6,  # cap bar thickness so the slot keeps air
    "area_alpha": 0.10,
    "wedge_ring_width": 2.0,
}


def _relative_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    channels = (int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linearize(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ink(hex_color):
    """Pick white or the dark ink for text set inside a fill of this color."""
    return CHROME["primary_ink"] if _relative_luminance(hex_color) > 0.4 else "#ffffff"


def require_series_capacity(n_series, *, max_series, chart_name):
    if n_series > max_series:
        raise ValueError(
            f"{chart_name}() supports at most {max_series} series before the "
            "validated color order runs out -- fold extra series into 'Other' "
            "or split into small multiples instead of adding another color."
        )
