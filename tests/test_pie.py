import pytest

import viscomm as vc
from viscomm.theme import CATEGORICAL


def test_pie_wedge_count_matches_labels():
    ax = vc.pie(["A", "B", "C"], [30, 50, 20])
    assert len(ax.patches) == 3


def test_mismatched_labels_values_raises():
    with pytest.raises(ValueError):
        vc.pie(["A", "B"], [1, 2, 3])


def test_too_many_slices_raises():
    with pytest.raises(ValueError):
        vc.pie([f"L{i}" for i in range(len(CATEGORICAL) + 1)], [1] * (len(CATEGORICAL) + 1))
