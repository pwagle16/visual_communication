import pytest

import viscomm as vc
from viscomm import theme


@pytest.fixture(autouse=True)
def _reset_theme():
    yield
    theme.set_theme("default")


def _facecolor_hex(patch):
    r, g, b, _ = patch.get_facecolor()
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def test_default_theme_is_active_initially():
    assert vc.active_theme() == "default"


def test_set_theme_switches_active_palette():
    vc.set_theme("pastel")
    assert vc.active_theme() == "pastel"
    assert vc.palette() == theme.THEMES["pastel"]


def test_unknown_theme_raises():
    with pytest.raises(ValueError):
        vc.set_theme("neon")
    with pytest.raises(ValueError):
        vc.palette("neon")


def test_per_chart_theme_overrides_active():
    vc.set_theme("default")
    ax = vc.bar(["A", "B"], values=[1, 2], theme="pastel")
    assert _facecolor_hex(ax.patches[0]) == theme.THEMES["pastel"][0]
    # active theme is untouched by the per-chart override
    assert vc.active_theme() == "default"


def test_active_theme_colors_used_when_no_override():
    vc.set_theme("pastel")
    ax = vc.bar(["A", "B"], values=[1, 2])
    assert _facecolor_hex(ax.patches[0]) == theme.THEMES["pastel"][0]


def test_both_themes_have_eight_distinct_hues():
    for name, hues in theme.THEMES.items():
        assert len(hues) == 8, name
        assert len(set(hues)) == 8, name
