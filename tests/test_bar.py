import pytest

import viscomm as vc
from viscomm import CATEGORICAL


def test_single_series_bar_has_no_legend():
    ax = vc.bar(["A", "B", "C"], values=[10, 20, 15])
    assert len(ax.patches) == 3
    assert ax.get_legend() is None


def test_single_series_uses_first_categorical_color():
    ax = vc.bar(["A", "B"], values=[1, 2])
    assert ax.patches[0].get_facecolor()[:3] == pytest.approx(_hex_to_rgb(CATEGORICAL[0]))


def test_grouped_series_gets_legend_and_fixed_color_order():
    ax = vc.bar(["A", "B"], series={"East": [1, 2], "West": [3, 4]})
    legend = ax.get_legend()
    assert legend is not None
    assert [t.get_text() for t in legend.get_texts()] == ["East", "West"]


def test_mismatched_series_length_raises():
    with pytest.raises(ValueError):
        vc.bar(["A", "B", "C"], values=[1, 2])


def test_requires_exactly_one_of_values_or_series():
    with pytest.raises(ValueError):
        vc.bar(["A"], values=[1], series={"x": [1]})
    with pytest.raises(ValueError):
        vc.bar(["A"])


def test_too_many_series_raises():
    with pytest.raises(ValueError):
        vc.bar(["A"], series={f"s{i}": [i] for i in range(len(CATEGORICAL) + 1)})


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))
