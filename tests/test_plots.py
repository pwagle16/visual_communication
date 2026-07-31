import pandas as pd
import pytest

import simple_eda as eda


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "name": ["Ana", "Bo", None],
            "age": [25, None, 31],
            "signups": [3, 5, 2],
        }
    )


def test_plot_missing_writes_file(df, tmp_path):
    path = tmp_path / "missing.png"
    result = eda.plot_missing(df, str(path))
    assert result == str(path)
    assert path.exists() and path.stat().st_size > 0


def test_plot_numeric_writes_file(df, tmp_path):
    path = tmp_path / "numeric.png"
    eda.plot_numeric(df, str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_histogram_writes_file(df, tmp_path):
    path = tmp_path / "hist.png"
    eda.plot_histogram(df, "age", str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_histogram_unknown_column(df, tmp_path):
    with pytest.raises(KeyError):
        eda.plot_histogram(df, "nope", str(tmp_path / "x.png"))


def test_plot_numeric_no_numeric_columns(tmp_path):
    df = pd.DataFrame({"name": ["a", "b"]})
    with pytest.raises(ValueError):
        eda.plot_numeric(df, str(tmp_path / "x.png"))


def test_plots_reject_non_dataframe(tmp_path):
    with pytest.raises(TypeError):
        eda.plot_missing([1, 2, 3], str(tmp_path / "x.png"))
