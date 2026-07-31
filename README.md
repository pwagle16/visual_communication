# simple_eda

The simplest possible exploratory-data-analysis helpers for pandas DataFrames.

- **Simple API** — flat, top-level functions. No classes to learn.
- **Boring names** — `summarize`, `missing`, `numeric_columns`.
- **Pandas in, plain objects out** — dicts, lists, ints, strings, and pandas Series.

## Install

```bash
pip install -e .
```

## Usage

```python
import pandas as pd
import simple_eda as eda

df = pd.DataFrame({
    "name": ["Ana", "Bo", None],
    "age": [25, None, 31],
})

print(eda.summarize(df))
# {'rows': 3, 'columns': 2, 'names': ['name', 'age']}

print(eda.numeric_columns(df))
# ['age']

print(eda.missing(df))
# name    1
# age     1
# dtype: int64
```

Or run it against the bundled dataset:

```bash
python examples/basic_usage.py
```

## API

| Function | Returns | Description |
| --- | --- | --- |
| `summarize(df)` | `dict` | `rows`, `columns`, and column `names`. |
| `missing(df)` | `pandas.Series` | Count of missing values per column. |
| `numeric_columns(df)` | `list` | Names of the numeric columns. |

All three accept a pandas `DataFrame` and raise `TypeError` on anything else.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
