"""Named visual styles for the charts.

A style is just a dict of colors and toggles. Pass a style name to any
plotting function (``style="dark"``). Palettes are colorblind-safe and were
checked with a palette validator; text stays on ink tokens, never a series hue.
"""

from __future__ import annotations

# Categorical hues, validated for each surface (light / dark).
_LIGHT_PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
_DARK_PALETTE = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

def _style(surface, ink, muted, palette, grid, spines, bar_edge, title_weight):
    return dict(surface=surface, ink=ink, muted=muted, palette=palette,
                grid=grid, spines=spines, bar_edge=bar_edge, title_weight=title_weight)


STYLES = {
    # Clean light surface with a soft grid.
    "light": _style("#fcfcfb", "#0b0b0b", "#52514e", _LIGHT_PALETTE, True, True, "white", "normal"),
    # Dark surface, hues re-stepped for it.
    "dark": _style("#1a1a19", "#ffffff", "#c3c2b7", _DARK_PALETTE, True, True, "#1a1a19", "normal"),
    # Stripped-down: single hue, no grid, no top/right spines.
    "minimal": _style("#ffffff", "#0b0b0b", "#52514e", ["#2a78d6"], False, False, "white", "normal"),
    # High-contrast, heavier titles, full palette.
    "bold": _style("#ffffff", "#000000", "#333333", _LIGHT_PALETTE, False, True, "black", "bold"),
}

DEFAULT_STYLE = "light"


def get_style(name: str) -> dict:
    """Return the style dict for ``name`` (raises ValueError if unknown)."""
    try:
        return STYLES[name]
    except KeyError:
        options = ", ".join(sorted(STYLES))
        raise ValueError(f"unknown style {name!r}; choose from: {options}")


def color(style: dict, i: int) -> str:
    """Nth palette color, wrapping if there are more marks than hues."""
    palette = style["palette"]
    return palette[i % len(palette)]


def apply(ax, fig, style: dict) -> None:
    """Apply surface, text, grid, and spine settings to an Axes/Figure."""
    fig.set_facecolor(style["surface"])
    ax.set_facecolor(style["surface"])
    for spine_name, spine in ax.spines.items():
        if not style["spines"] and spine_name in ("top", "right"):
            spine.set_visible(False)
        else:
            spine.set_color(style["muted"])
    ax.tick_params(colors=style["muted"])
    for label in (ax.xaxis.label, ax.yaxis.label):
        label.set_color(style["ink"])
    if style["grid"]:
        ax.grid(True, axis="y", color=style["muted"], alpha=0.2, linewidth=0.8)
        ax.set_axisbelow(True)
