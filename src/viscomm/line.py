from ._mpl import add_legend, apply_base_style, new_axes, set_axis_labels, style_title
from .theme import CHROME, MARK, palette, require_series_capacity

# Past this many converging series, end-labels collide; fall back to the
# legend alone rather than stack labels on top of each other.
DIRECT_LABEL_MAX_SERIES = 4


def line(
    x,
    y=None,
    *,
    series=None,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    direct_labels=True,
    theme=None,
    ax=None,
    figsize=(8, 5),
):
    """A line chart. Pass `y` for a single series, or `series` (dict of
    name -> y-values) for multiple lines sharing the same x-axis.
    `theme` overrides the active theme for this chart only."""
    if (y is None) == (series is None):
        raise ValueError("Pass exactly one of `y` or `series`.")

    if series is None:
        series = {"": y}

    colors = palette(theme)
    require_series_capacity(len(series), max_series=len(colors), chart_name="line")

    for name, ys in series.items():
        if len(ys) != len(x):
            raise ValueError(f"series '{name}' has {len(ys)} values, expected {len(x)}.")

    if ax is None:
        fig, ax = new_axes(figsize)
    else:
        fig = ax.figure

    show_direct_labels = direct_labels and len(series) <= DIRECT_LABEL_MAX_SERIES

    for i, (name, ys) in enumerate(series.items()):
        color = colors[i]
        ax.plot(
            x, ys, color=color, linewidth=MARK["line_width"],
            solid_capstyle="round", solid_joinstyle="round",
            label=name or None, zorder=3,
        )
        end_x, end_y = x[-1], ys[-1]
        ax.plot(
            [end_x], [end_y], marker="o", markersize=MARK["marker_size"],
            markerfacecolor=color, markeredgecolor=CHROME["surface"],
            markeredgewidth=MARK["marker_ring_width"], zorder=4,
        )
        if show_direct_labels:
            ax.annotate(
                name if name else f"{end_y:g}",
                (end_x, end_y), xytext=(8, 0), textcoords="offset points",
                va="center", color=CHROME["secondary_ink"], fontsize=9,
            )

    apply_base_style(ax, grid_axis="y")
    style_title(ax, title, subtitle)
    set_axis_labels(ax, xlabel, ylabel)
    # Legend stays the dependable identity channel; direct labels only supplement
    # it, but they sit at the right edge, so keep the legend off that side.
    add_legend(ax, len(series), placement="bottom" if show_direct_labels else "right")
    fig.tight_layout()
    return ax
