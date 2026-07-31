import pytest

import viscomm as vc

SCATTER_MAX_SERIES = 3


def test_single_group_no_legend():
    ax = vc.scatter([1, 2, 3], [4, 5, 6])
    assert ax.get_legend() is None
    assert len(ax.collections) == 1


def test_multi_group_gets_legend():
    ax = vc.scatter(None, None, series={"A": ([1, 2], [1, 2]), "B": ([3, 4], [3, 4])})
    legend = ax.get_legend()
    assert legend is not None
    assert [t.get_text() for t in legend.get_texts()] == ["A", "B"]


def test_mismatched_xy_length_raises():
    with pytest.raises(ValueError):
        vc.scatter([1, 2, 3], [1, 2])


def test_exceeds_all_pairs_cap_raises():
    series = {f"s{i}": ([1], [1]) for i in range(SCATTER_MAX_SERIES + 1)}
    with pytest.raises(ValueError):
        vc.scatter(None, None, series=series)
