"""Validated default theme: categorical palette, chrome colors, mark specs.

Colors and mark specs are the reference palette from the dataviz design
method (see project README) -- an eight-hue categorical order validated for
colorblind-safe adjacent pairs, plus fixed chrome tokens for chart chrome
(gridlines, axes, ink). Swap the values below to re-theme; the chart
functions in bar.py/line.py/scatter.py/pie.py consume them by role, not by
raw hex, so nothing else needs to change.
"""

# Fixed hue order -- never cycled. Assigned to series by position, in the
# order series are given. Bar/line tolerate all 8 slots (adjacent-pair
# validation); scatter caps at 3 (all-pairs validation) -- see scatter.py.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

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
