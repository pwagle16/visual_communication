"""Shared matplotlib plumbing so every chart type looks like one system."""

import matplotlib
import matplotlib.pyplot as plt

from .theme import CHROME

# Register a cross-platform sans-serif preference order as the *fallback list*
# for the generic "sans-serif" family, then always ask artists for the generic
# family. matplotlib walks this list and silently uses the first font that
# exists (DejaVu Sans ships with matplotlib, so the list never comes up empty).
# Passing an explicit list to an artist instead would log a "Font family not
# found" warning for every missing name on the platform -- dozens per figure
# on Linux/CI, where Segoe UI/Helvetica/Arial are all absent.
_SANS_PREF = ["Segoe UI", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = _SANS_PREF + [
    f for f in matplotlib.rcParams["font.sans-serif"] if f not in _SANS_PREF
]

_SANS = "sans-serif"  # generic family alias -> resolved via the fallback list above


def new_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(CHROME["surface"])
    ax.set_facecolor(CHROME["surface"])
    return fig, ax


def apply_base_style(ax, *, grid_axis="y"):
    for name, spine in ax.spines.items():
        if name in ("top", "right"):
            spine.set_visible(False)
        else:
            spine.set_color(CHROME["baseline"])
            spine.set_linewidth(1.0)

    ax.tick_params(colors=CHROME["muted_ink"], labelsize=9, length=0)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(CHROME["secondary_ink"])
        label.set_fontfamily(_SANS)

    if grid_axis:
        ax.grid(axis=grid_axis, color=CHROME["gridline"], linewidth=1.0, zorder=0)
    ax.set_axisbelow(True)


def style_title(ax, title=None, subtitle=None):
    if title:
        ax.text(
            0, 1.12, title, transform=ax.transAxes,
            fontsize=13, fontweight="bold", color=CHROME["primary_ink"],
            fontfamily=_SANS, ha="left", va="bottom",
        )
    if subtitle:
        ax.text(
            0, 1.02, subtitle, transform=ax.transAxes,
            fontsize=10, color=CHROME["secondary_ink"],
            fontfamily=_SANS, ha="left", va="bottom",
        )


def add_legend(ax, n_series, *, placement="right"):
    """A legend is always present for >= 2 series, never for one.

    `placement="right"` puts it outside the axes at the top right (the
    default). `placement="bottom"` puts it below the axes instead -- use
    this when the chart also carries right-edge direct labels (e.g. line
    end-labels), so the two don't collide.
    """
    existing = ax.get_legend()
    if existing:
        existing.remove()
    if n_series < 2:
        return
    if placement == "bottom":
        ax.legend(
            frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12),
            ncol=min(n_series, 4), labelcolor=CHROME["secondary_ink"], fontsize=9,
        )
    else:
        ax.legend(
            frameon=False, loc="upper left", bbox_to_anchor=(1.02, 1),
            labelcolor=CHROME["secondary_ink"], fontsize=9,
        )


def set_axis_labels(ax, xlabel=None, ylabel=None):
    if xlabel:
        ax.set_xlabel(xlabel, color=CHROME["secondary_ink"], fontsize=10, fontfamily=_SANS)
    if ylabel:
        ax.set_ylabel(ylabel, color=CHROME["secondary_ink"], fontsize=10, fontfamily=_SANS)
