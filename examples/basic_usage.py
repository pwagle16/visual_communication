"""Run simple_eda on the bundled dataset: text summaries + charts.

    python examples/basic_usage.py

Charts are written to examples/output/.
"""

from pathlib import Path

import pandas as pd

import simple_eda as eda

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "people.csv"
OUT = ROOT / "examples" / "output"


def main() -> None:
    df = pd.read_csv(DATA)

    # text summaries
    print("summarize:", eda.summarize(df))
    print("numeric_columns:", eda.numeric_columns(df))
    print("missing:")
    print(eda.missing(df))

    # visuals
    OUT.mkdir(exist_ok=True)
    print("saved:", eda.plot_missing(df, str(OUT / "missing.png")))
    print("saved:", eda.plot_numeric(df, str(OUT / "numeric.png")))
    print("saved:", eda.plot_histogram(df, "age", str(OUT / "age_hist.png")))


if __name__ == "__main__":
    main()
