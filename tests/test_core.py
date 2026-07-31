import pandas as pd
import pytest

import simple_eda as eda


@pytest.fixture
def df():
    # Mirrors the tiny DataFrame from the slides, plus a numeric column.
    return pd.DataFrame(
        {
            "name": ["Ana", "Bo", None],
            "age": [25, None, 31],
            "signups": [3, 5, 2],
        }
    )


def test_summarize_shape_and_names(df):
    assert eda.summarize(df) == {
        "rows": 3,
        "columns": 3,
        "names": ["name", "age", "signups"],
    }


def test_summarize_returns_plain_types(df):
    result = eda.summarize(df)
    assert isinstance(result, dict)
    assert isinstance(result["rows"], int)
    assert isinstance(result["names"], list)


def test_missing_counts_per_column(df):
    result = eda.missing(df)
    assert isinstance(result, pd.Series)
    assert result["name"] == 1
    assert result["age"] == 1
    assert result["signups"] == 0


def test_numeric_columns(df):
    assert eda.numeric_columns(df) == ["age", "signups"]


def test_empty_dataframe():
    empty = pd.DataFrame()
    assert eda.summarize(empty) == {"rows": 0, "columns": 0, "names": []}
    assert eda.numeric_columns(empty) == []


@pytest.mark.parametrize("func", [eda.summarize, eda.missing, eda.numeric_columns])
def test_rejects_non_dataframe(func):
    with pytest.raises(TypeError):
        func([1, 2, 3])
