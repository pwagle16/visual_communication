import numpy as np

from ._mpl import add_legend, apply_base_style, new_axes, set_axis_labels, style_title
from .theme import CATEGORICAL, MARK, require_series_capacity


def bar(
    categories,
    values=None,
    *,
    series=None,
    horizontal=False,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    ax=None,
    figsize=(8, 5),
):
    """A bar/column chart. One measure, one axis.

    Pass either `values` (a single series) or `series` (a dict mapping
    series name -> list of values, one grouped bar cluster per category).
    """
    if (values is None) == (series is None):
        raise ValueError("Pass exactly one of `values` or `series`.")

    if series is None:
        series = {"": values}

    require_series_capacity(len(series), max_series=len(CATEGORICAL), chart_name="bar")

    n_categories = len(categories)
    n_series = len(series)
    for name, vals in series.items():
        if len(vals) != n_categories:
            raise ValueError(f"series '{name}' has {len(vals)} values, expected {n_categories}.")

    if ax is None:
        fig, ax = new_axes(figsize)
    else:
        fig = ax.figure

    x = np.arange(n_categories)
    slot_width = 0.8  # leftover 0.2 of the slot stays air, per bar spec
    bar_width = min(MARK["bar_max_width_frac"], slot_width / n_series)

    for i, (name, vals) in enumerate(series.items()):
        offset = (i - (n_series - 1) / 2) * bar_width
        if horizontal:
            ax.barh(x + offset, vals, height=bar_width, color=CATEGORICAL[i], label=name or None, zorder=3)
        else:
            ax.bar(x + offset, vals, width=bar_width, color=CATEGORICAL[i], label=name or None, zorder=3)

    ticks_setter = ax.set_yticks if horizontal else ax.set_xticks
    labels_setter = ax.set_yticklabels if horizontal else ax.set_xticklabels
    ticks_setter(x)
    labels_setter(categories)

    apply_base_style(ax, grid_axis="x" if horizontal else "y")
    style_title(ax, title, subtitle)
    set_axis_labels(ax, xlabel, ylabel)
    add_legend(ax, n_series)
    fig.tight_layout()
    return ax
