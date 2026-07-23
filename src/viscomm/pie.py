from ._mpl import new_axes, style_title
from .theme import CHROME, MARK, contrast_ink, palette, require_series_capacity


def pie(labels, values, *, title=None, subtitle=None, theme=None, ax=None, figsize=(6, 6)):
    """A pie chart with direct-labeled, percentage-annotated wedges.
    `theme` overrides the active theme for this chart only."""
    if len(labels) != len(values):
        raise ValueError(f"got {len(labels)} labels but {len(values)} values.")

    theme_colors = palette(theme)
    require_series_capacity(len(labels), max_series=len(theme_colors), chart_name="pie")

    if ax is None:
        fig, ax = new_axes(figsize)
    else:
        fig = ax.figure

    colors = theme_colors[: len(labels)]
    _wedges, _texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.0f%%",
        pctdistance=0.75,
        startangle=90,
        counterclock=False,
        wedgeprops={"linewidth": MARK["wedge_ring_width"], "edgecolor": CHROME["surface"]},
        textprops={"color": CHROME["secondary_ink"], "fontsize": 9},
    )
    for color, autotext in zip(colors, autotexts):
        autotext.set_color(contrast_ink(color))

    ax.set_aspect("equal")
    style_title(ax, title, subtitle)
    fig.tight_layout()
    return ax
