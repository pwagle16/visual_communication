"""viscomm core -- four chart types over matplotlib with one shared look.

Everything lives here: the palette, the chrome colors, the styling helpers,
and the `bar`/`line`/`scatter`/`pie` functions. Charts consume colors by role
(a series is the Nth palette hue), never by raw hex, so the whole set reads as
one system. Every function returns the matplotlib Axes, so charts compose onto
a shared figure with the `ax=` argument.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# A coffee-brown categorical order, assigned to series by position. The first
# slot is a dark espresso so the leading series stands out; the rest are warmer
# browns. Capped at eight: past that, fold extras into "Other".
CATEGORICAL = [
    "#3b2412",  # espresso (stands out)
    "#6f4a29",  # coffee
    "#a9855f",  # latte
    "#caa877",  # foam tan
    "#8a5a34",  # mocha
    "#d8c3a5",  # oat
    "#5b3a22",  # roast
    "#b58a63",  # caramel
]

# Non-data "chrome": a warm latte surface, espresso ink, and crema-toned lines.
CHROME = {
    "surface": "#f2e8d5",
    "primary_ink": "#2e1c0d",
    "secondary_ink": "#5f4025",
    "muted_ink": "#8a6a4a",
    "gridline": "#e0d0b4",
    "baseline": "#c2a279",
}

_LINE_WIDTH = 2.0
_MARKER_SIZE = 8.0
_RING_WIDTH = 2.0

# Prefer common sans fonts but fall back through matplotlib's own bundled
# DejaVu Sans, so missing platform fonts never spam warnings.
_SANS = ["Segoe UI", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = _SANS + [
    f for f in matplotlib.rcParams["font.sans-serif"] if f not in _SANS
]


def contrast_ink(hex_color):
    """White or dark ink for text set on a fill of this color (WCAG luminance)."""
    h = hex_color.lstrip("#")
    chan = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in chan)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return CHROME["primary_ink"] if luminance > 0.4 else "#ffffff"


def _check_capacity(n, chart):
    if n > len(CATEGORICAL):
        raise ValueError(
            f"{chart}() supports at most {len(CATEGORICAL)} series before the "
            "validated color order runs out -- fold extras into 'Other'."
        )


def _new_axes(ax, figsize):
    if ax is not None:
        return ax
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(CHROME["surface"])
    ax.set_facecolor(CHROME["surface"])
    return ax


def _style(ax, *, title, subtitle, xlabel, ylabel, grid_axis="y"):
    """Apply the shared frame: spines, ticks, grid, titles, axis labels."""
    for name, spine in ax.spines.items():
        if name in ("top", "right"):
            spine.set_visible(False)
        else:
            spine.set_color(CHROME["baseline"])
    ax.tick_params(colors=CHROME["muted_ink"], labelsize=9, length=0)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(CHROME["secondary_ink"])
    if grid_axis:
        ax.grid(axis=grid_axis, color=CHROME["gridline"], linewidth=1.0, zorder=0)
    ax.set_axisbelow(True)
    if title:
        ax.text(0, 1.12, title, transform=ax.transAxes, fontsize=13,
                fontweight="bold", color=CHROME["primary_ink"], ha="left", va="bottom")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=10,
                color=CHROME["secondary_ink"], ha="left", va="bottom")
    if xlabel:
        ax.set_xlabel(xlabel, color=CHROME["secondary_ink"], fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color=CHROME["secondary_ink"], fontsize=10)


def _legend(ax, n_series, *, placement="right"):
    """Identity channel for 2+ series; never drawn for a single series."""
    if n_series < 2:
        return
    if placement == "bottom":
        ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12),
                  ncol=min(n_series, 4), labelcolor=CHROME["secondary_ink"], fontsize=9)
    else:
        ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.02, 1),
                  labelcolor=CHROME["secondary_ink"], fontsize=9)


def _as_series(single, series, single_name):
    """Normalize the single-vs-multi calling convention to a dict of series."""
    if (single is None) == (series is None):
        raise ValueError(f"Pass exactly one of `{single_name}` or `series`.")
    return {"": single} if series is None else series


# --- coffee beans -----------------------------------------------------------
# The signature garnish: every chart the library draws gets roasted coffee
# beans tucked into its corners. A bean is an ellipse plus a curved seam;
# offsets are divided by the figure's inch size so beans stay bean-shaped on
# any aspect ratio. Corners are chosen because they stay clear of titles,
# legends, and axis labels whatever the data.
_BEAN_ROASTS = ["#3d2415", "#4a2f1a", "#5b3a22", "#33200f"]
_BEAN_SPOTS = [  # (x, y, angle) in figure fractions, tucked clear of text
    (0.035, 0.05, 25), (0.085, 0.115, 60),   # bottom-left
    (0.965, 0.05, 40), (0.915, 0.115, 85),   # bottom-right
    (0.965, 0.95, 15), (0.915, 0.90, 130),   # top-right
    (0.03, 0.965, 110),                       # top-left, above the title
]


def _draw_bean(deco, fx, fy, size, angle, fill, w, h):
    a = np.radians(angle)
    ca, sa = np.cos(a), np.sin(a)
    t = np.linspace(0, 2 * np.pi, 40)
    ox, oy = np.cos(t) * size, np.sin(t) * size * 0.6
    deco.fill(fx + (ox * ca - oy * sa) / w, fy + (ox * sa + oy * ca) / h,
              facecolor=fill, edgecolor="#20120a", linewidth=1.0, zorder=5)
    s = np.linspace(-0.8, 0.8, 20)
    sx, sy = s * size, np.sin(s * np.pi) * 0.12 * size  # gentle bow for the seam
    deco.plot(fx + (sx * ca - sy * sa) / w, fy + (sx * sa + sy * ca) / h,
              color="#c8a877", linewidth=1.1, zorder=6, solid_capstyle="round")


def _coffee_beans(fig):
    """Scatter coffee beans into the corners of a figure the library owns."""
    w, h = fig.get_size_inches()
    deco = fig.add_axes((0, 0, 1, 1), zorder=5)
    deco.set_axis_off()
    deco.set_xlim(0, 1)
    deco.set_ylim(0, 1)
    deco.patch.set_alpha(0)
    for i, (fx, fy, ang) in enumerate(_BEAN_SPOTS):
        _draw_bean(deco, fx, fy, 0.20 + 0.03 * (i % 3), ang, _BEAN_ROASTS[i % 4], w, h)


def bar(categories, values=None, *, series=None, colors=None, horizontal=False,
        title=None, subtitle=None, xlabel=None, ylabel=None, ax=None, figsize=(8, 5)):
    """Bar/column chart. Pass `values` for one series, or `series` (name ->
    values) for grouped bars. `colors` overrides the default palette: a list
    of one color per bar for a single series, or one per series when grouped.
    Returns the Axes."""
    series = _as_series(values, series, "values")
    _check_capacity(len(series), "bar")
    n_cat, n_series = len(categories), len(series)
    for name, vals in series.items():
        if len(vals) != n_cat:
            raise ValueError(f"series '{name}' has {len(vals)} values, expected {n_cat}.")
    owns = ax is None
    ax = _new_axes(ax, figsize)
    per_bar = colors is not None and n_series == 1  # one color per bar, not per series

    x = np.arange(n_cat)
    pitch = 0.8 / n_series  # cluster fills 80% of each category slot
    gap = 0.12 * pitch if n_series > 1 else 0.0  # thin surface gap between bars
    width = min(0.6, pitch - gap)
    for i, (name, vals) in enumerate(series.items()):
        offset = (i - (n_series - 1) / 2) * pitch
        color = colors if per_bar else (colors or CATEGORICAL)[i]
        draw = ax.barh if horizontal else ax.bar
        key = "height" if horizontal else "width"
        draw(x + offset, vals, label=name or None, color=color, zorder=3, **{key: width})
    (ax.set_yticks if horizontal else ax.set_xticks)(x)
    (ax.set_yticklabels if horizontal else ax.set_xticklabels)(categories)

    _style(ax, title=title, subtitle=subtitle, xlabel=xlabel, ylabel=ylabel,
           grid_axis="x" if horizontal else "y")
    _legend(ax, n_series)
    fig = ax.figure
    fig.tight_layout()
    if owns:
        _coffee_beans(fig)
    return ax


def line(x, y=None, *, series=None, colors=None, title=None, subtitle=None,
         xlabel=None, ylabel=None, direct_labels=True, ax=None, figsize=(8, 5)):
    """Line chart. Pass `y` for one series, or `series` (name -> y-values)
    sharing the x-axis. `colors` overrides the default palette (one per
    series). End markers and direct labels supplement the legend.
    Returns the Axes."""
    series = _as_series(y, series, "y")
    _check_capacity(len(series), "line")
    for name, ys in series.items():
        if len(ys) != len(x):
            raise ValueError(f"series '{name}' has {len(ys)} values, expected {len(x)}.")
    owns = ax is None
    ax = _new_axes(ax, figsize)

    labelled = direct_labels and len(series) <= 4  # past 4, end-labels collide
    for i, (name, ys) in enumerate(series.items()):
        color = (colors or CATEGORICAL)[i]
        ax.plot(x, ys, color=color, linewidth=_LINE_WIDTH, solid_capstyle="round",
                solid_joinstyle="round", label=name or None, zorder=3)
        ax.plot([x[-1]], [ys[-1]], marker="o", markersize=_MARKER_SIZE,
                markerfacecolor=color, markeredgecolor=CHROME["surface"],
                markeredgewidth=_RING_WIDTH, zorder=4)
        if labelled:
            ax.annotate(name or f"{ys[-1]:g}", (x[-1], ys[-1]), xytext=(8, 0),
                        textcoords="offset points", va="center",
                        color=CHROME["secondary_ink"], fontsize=9)

    _style(ax, title=title, subtitle=subtitle, xlabel=xlabel, ylabel=ylabel)
    _legend(ax, len(series), placement="bottom" if labelled else "right")
    fig = ax.figure
    fig.tight_layout()
    if owns:
        _coffee_beans(fig)
    return ax


def scatter(x, y=None, *, series=None, title=None, subtitle=None, xlabel=None,
            ylabel=None, ax=None, figsize=(8, 5)):
    """Scatter plot. Pass `x`/`y` for one group, or `series` (name -> (xs, ys))
    for multiple. Capped at 3 groups (all-pairs color validation). Returns the Axes."""
    series = _as_series(None if y is None else (x, y), series, "y")
    if len(series) > 3:
        raise ValueError("scatter() supports at most 3 groups before adjacent "
                         "points become hard to tell apart by color.")
    owns = ax is None
    ax = _new_axes(ax, figsize)

    marker_area = _MARKER_SIZE ** 2  # matplotlib `s` is area in points**2
    for i, (name, (xs, ys)) in enumerate(series.items()):
        if len(xs) != len(ys):
            raise ValueError(f"series '{name}' has mismatched x ({len(xs)}) / y ({len(ys)}).")
        ax.scatter(xs, ys, s=marker_area, color=CATEGORICAL[i], edgecolors=CHROME["surface"],
                   linewidths=_RING_WIDTH, label=name or None, zorder=3)

    _style(ax, title=title, subtitle=subtitle, xlabel=xlabel, ylabel=ylabel)
    _legend(ax, len(series))
    fig = ax.figure
    fig.tight_layout()
    if owns:
        _coffee_beans(fig)
    return ax


def pie(labels, values, *, title=None, subtitle=None, ax=None, figsize=(6, 6)):
    """Pie chart with direct-labeled, percentage-annotated wedges. Returns the Axes."""
    if len(labels) != len(values):
        raise ValueError(f"got {len(labels)} labels but {len(values)} values.")
    _check_capacity(len(labels), "pie")
    owns = ax is None
    ax = _new_axes(ax, figsize)

    colors = CATEGORICAL[: len(labels)]
    _wedges, _texts, autotexts = ax.pie(
        values, labels=labels, colors=colors, autopct="%1.0f%%", pctdistance=0.75,
        startangle=90, counterclock=False,
        wedgeprops={"linewidth": _RING_WIDTH, "edgecolor": CHROME["surface"]},
        textprops={"color": CHROME["secondary_ink"], "fontsize": 9},
    )
    for color, autotext in zip(colors, autotexts):
        autotext.set_color(contrast_ink(color))
    ax.set_aspect("equal")
    _style(ax, title=title, subtitle=subtitle, xlabel=None, ylabel=None, grid_axis=None)
    fig = ax.figure
    fig.tight_layout()
    if owns:
        _coffee_beans(fig)
    return ax
