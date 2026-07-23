from ._mpl import add_legend, apply_base_style, new_axes, set_axis_labels, style_title
from .theme import CATEGORICAL, CHROME, MARK, SCATTER_MAX_SERIES, require_series_capacity


def scatter(
    x,
    y=None,
    *,
    series=None,
    title=None,
    subtitle=None,
    xlabel=None,
    ylabel=None,
    ax=None,
    figsize=(8, 5),
):
    """A scatter plot. Pass `x`/`y` for a single group, or `series` (dict of
    name -> (x_values, y_values)) for multiple groups.

    Capped at 3 groups: scatter shows every pair of points at once, so the
    palette's all-pairs colorblind validation (not just adjacent-pair) is
    what applies, and only the first 3 slots clear that bar.
    """
    if (y is None) == (series is None):
        raise ValueError("Pass exactly one of `y` or `series`.")

    if series is None:
        series = {"": (x, y)}

    require_series_capacity(len(series), max_series=SCATTER_MAX_SERIES, chart_name="scatter")

    if ax is None:
        fig, ax = new_axes(figsize)
    else:
        fig = ax.figure

    # matplotlib's `s` is marker area in points**2; squaring the target
    # diameter gives roughly that diameter on screen.
    marker_area = MARK["marker_size"] ** 2
    for i, (name, (xs, ys)) in enumerate(series.items()):
        if len(xs) != len(ys):
            raise ValueError(f"series '{name}' has mismatched x ({len(xs)}) and y ({len(ys)}) lengths.")
        ax.scatter(
            xs, ys, s=marker_area, color=CATEGORICAL[i],
            edgecolors=CHROME["surface"], linewidths=MARK["marker_ring_width"],
            label=name or None, zorder=3,
        )

    apply_base_style(ax, grid_axis="y")
    style_title(ax, title, subtitle)
    set_axis_labels(ax, xlabel, ylabel)
    add_legend(ax, len(series))
    fig.tight_layout()
    return ax
