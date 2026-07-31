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


@pytest.mark.parametrize("style", ["light", "dark", "minimal", "bold"])
def test_every_style_renders(df, tmp_path, style):
    path = tmp_path / f"{style}.png"
    eda.plot_missing(df, str(path), style=style)
    assert path.exists() and path.stat().st_size > 0


def test_unknown_style_raises(df, tmp_path):
    with pytest.raises(ValueError):
        eda.plot_missing(df, str(tmp_path / "x.png"), style="rainbow")


def test_plot_scatter_writes_file(df, tmp_path):
    path = tmp_path / "scatter.png"
    eda.plot_scatter(df, "age", "signups", str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_scatter_unknown_column(df, tmp_path):
    with pytest.raises(KeyError):
        eda.plot_scatter(df, "age", "nope", str(tmp_path / "x.png"))


def test_plot_line_single_and_multi(tmp_path):
    ts = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "a": [1, 2, 3], "b": [3, 2, 4]})
    p1 = tmp_path / "line1.png"
    p2 = tmp_path / "line2.png"
    eda.plot_line(ts, "month", "a", str(p1))
    eda.plot_line(ts, "month", ["a", "b"], str(p2))
    assert p1.exists() and p2.exists()


def test_plot_correlation_writes_file(df, tmp_path):
    path = tmp_path / "corr.png"
    eda.plot_correlation(df, str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_correlation_needs_two_numeric(tmp_path):
    df = pd.DataFrame({"age": [1, 2, 3]})
    with pytest.raises(ValueError):
        eda.plot_correlation(df, str(tmp_path / "x.png"))


@pytest.fixture
def grouped():
    return pd.DataFrame(
        {
            "arm": ["A", "A", "B", "B", "A", "B"],
            "diet": ["Yes", "No", "Yes", "No", "Yes", "No"],
            "drop": [10.0, 6.0, 8.0, 4.0, 12.0, 5.0],
        }
    )


def test_plot_bar_simple(grouped, tmp_path):
    path = tmp_path / "bar.png"
    eda.plot_bar(grouped, "arm", "drop", path=str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_bar_grouped(grouped, tmp_path):
    path = tmp_path / "grouped.png"
    eda.plot_bar(grouped, "arm", "drop", group="diet", path=str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_box(grouped, tmp_path):
    path = tmp_path / "box.png"
    eda.plot_box(grouped, "arm", "drop", str(path))
    assert path.exists() and path.stat().st_size > 0


def test_plot_bar_unknown_column(grouped, tmp_path):
    with pytest.raises(KeyError):
        eda.plot_bar(grouped, "arm", "nope", path=str(tmp_path / "x.png"))
