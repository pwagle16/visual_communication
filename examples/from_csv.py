"""Load data/coffee_sales.csv and render one of each viscomm chart type.

Reads with the standard-library csv module (viscomm takes plain lists, so
no pandas needed -- though `pandas.read_csv` works just as well). Writes a
2x2 dashboard plus one PNG per chart into examples/output/.
"""

import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

import viscomm as vc

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(os.path.dirname(HERE), "data", "coffee_sales.csv")
OUT_DIR = os.path.join(HERE, "output")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_rows():
    with open(CSV_PATH, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:  # csv gives strings; cast the numeric columns
        r["revenue_k"] = float(r["revenue_k"])
        r["orders"] = int(r["orders"])
        r["ad_spend_k"] = float(r["ad_spend_k"])
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = load_rows()
    regions = sorted({r["region"] for r in rows})

    # line: monthly revenue per region -> one series per region.
    by_region_month = defaultdict(dict)
    for r in rows:
        by_region_month[r["region"]][r["month"]] = r["revenue_k"]
    revenue_series = {reg: [by_region_month[reg][m] for m in MONTHS] for reg in regions}

    # bar + pie: total revenue per region.
    totals = {reg: round(sum(revenue_series[reg]), 1) for reg in regions}

    # scatter: ad spend vs revenue, every region-month as one point.
    ad_spend = [r["ad_spend_k"] for r in rows]
    revenue = [r["revenue_k"] for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(vc.CHROME["surface"])

    vc.line(list(range(1, 13)), series=revenue_series,
            title="Monthly revenue by region", subtitle="$K, Jan-Dec",
            xlabel="Month", ylabel="$K", ax=axes[0, 0])
    vc.bar(regions, values=[totals[r] for r in regions],
           title="Total revenue by region", subtitle="$K, full year",
           ylabel="$K", ax=axes[0, 1])
    vc.scatter(ad_spend, revenue,
               title="Ad spend vs. revenue", xlabel="Ad spend ($K)",
               ylabel="Revenue ($K)", ax=axes[1, 0])
    vc.pie(regions, [totals[r] for r in regions],
           title="Revenue share by region", ax=axes[1, 1])

    fig.suptitle("Coffee sales -- from data/coffee_sales.csv", x=0.02, ha="left",
                 fontsize=15, fontweight="bold", color=vc.CHROME["primary_ink"])
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_path = os.path.join(OUT_DIR, "coffee_sales.png")
    fig.savefig(out_path, dpi=150)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
