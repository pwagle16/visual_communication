"""Run simple_eda on the bundled dataset: text summaries + charts.

    python examples/basic_usage.py

Charts are written to examples/output/.
"""

from pathlib import Path

import pandas as pd

import simple_eda as eda

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "people.csv"
SALES = ROOT / "data" / "sales.csv"
OUT = ROOT / "examples" / "output"


def main() -> None:
    df = pd.read_csv(DATA)
    sales = pd.read_csv(SALES)
    OUT.mkdir(exist_ok=True)

    # text summaries
    print("summarize:", eda.summarize(df))
    print("numeric_columns:", eda.numeric_columns(df))
    print("missing:")
    print(eda.missing(df))

    # the same bar chart in every visual style
    for style in eda.STYLES:
        print("saved:", eda.plot_missing(df, str(OUT / f"missing_{style}.png"), style=style))

    # different chart types
    print("saved:", eda.plot_histogram(df, "age", str(OUT / "age_hist.png")))
    print("saved:", eda.plot_numeric(df, str(OUT / "numeric.png")))
    print("saved:", eda.plot_scatter(sales, "ad_spend", "revenue", str(OUT / "scatter.png")))
    print("saved:", eda.plot_line(sales, "month", ["revenue", "ad_spend"], str(OUT / "line.png")))
    print("saved:", eda.plot_correlation(sales, str(OUT / "corr.png")))


if __name__ == "__main__":
    main()
