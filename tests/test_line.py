import pytest

import viscomm as vc
from viscomm import CATEGORICAL


def test_single_series_line_no_legend():
    ax = vc.line([1, 2, 3], y=[1, 4, 9])
    assert ax.get_legend() is None
    assert len(ax.lines) >= 1


def test_multi_series_line_gets_legend():
    ax = vc.line([1, 2, 3], series={"A": [1, 2, 3], "B": [3, 2, 1]})
    legend = ax.get_legend()
    assert legend is not None
    assert [t.get_text() for t in legend.get_texts()] == ["A", "B"]


def test_mismatched_length_raises():
    with pytest.raises(ValueError):
        vc.line([1, 2, 3], y=[1, 2])


def test_requires_exactly_one_of_y_or_series():
    with pytest.raises(ValueError):
        vc.line([1], y=[1], series={"x": [1]})
    with pytest.raises(ValueError):
        vc.line([1])


def test_too_many_series_raises():
    with pytest.raises(ValueError):
        vc.line([1], series={f"s{i}": [1] for i in range(len(CATEGORICAL) + 1)})
