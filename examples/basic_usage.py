"""Run the three simple_eda helpers on the bundled dataset.

    python examples/basic_usage.py
"""

from pathlib import Path

import pandas as pd

import simple_eda as eda

DATA = Path(__file__).resolve().parent.parent / "data" / "people.csv"


def main() -> None:
    df = pd.read_csv(DATA)

    print("summarize:", eda.summarize(df))
    print("numeric_columns:", eda.numeric_columns(df))
    print("missing:")
    print(eda.missing(df))


if __name__ == "__main__":
    main()
