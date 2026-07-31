"""Load data/coffee_sales.csv and render two charts with a brown palette.

Reads with the standard-library csv module (viscomm takes plain lists, so
no pandas needed). Renders monthly revenue lines per region alongside a
total-revenue bar chart, using a soft brown pastel palette -- with the
highest-revenue region drawn in dark brown to make it stand out. Colors are
mapped per region, so a region keeps the same color across both charts.
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

# Soft brown pastels for the also-rans; the top region gets dark brown.
BROWN_PASTEL = ["#cdb391", "#c2a279", "#dac7a8", "#b89b74"]
DARK_BROWN = "#4a2f1a"


def load_rows():
    with open(CSV_PATH, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:  # csv gives strings; cast the numeric columns
        r["revenue_k"] = float(r["revenue_k"])
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = load_rows()
    regions = sorted({r["region"] for r in rows})

    # Monthly revenue per region -> one line series per region.
    by_region_month = defaultdict(dict)
    for r in rows:
        by_region_month[r["region"]][r["month"]] = r["revenue_k"]
    revenue_series = {reg: [by_region_month[reg][m] for m in MONTHS] for reg in regions}

    # Total revenue per region drives the bar chart and picks the top region.
    totals = {reg: round(sum(revenue_series[reg]), 1) for reg in regions}
    top_region = max(totals, key=totals.get)

    # One color per region: dark brown for the leader, pastels for the rest.
    # Built in `regions` order so it lines up with both the line series and
    # the bar categories -- a region is the same color in both charts.
    pastels = iter(BROWN_PASTEL)
    region_color = {
        reg: DARK_BROWN if reg == top_region else next(pastels) for reg in regions
    }
    colors = [region_color[reg] for reg in regions]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor(vc.CHROME["surface"])

    vc.line(list(range(1, 13)), series=revenue_series, colors=colors,
            title="Monthly revenue by region", subtitle="$K, Jan-Dec",
            xlabel="Month", ylabel="$K", ax=axes[0])
    vc.bar(regions, values=[totals[r] for r in regions], colors=colors,
           title="Total revenue by region", subtitle=f"$K, full year -- {top_region} leads",
           ylabel="$K", ax=axes[1])

    fig.suptitle("Coffee sales -- from data/coffee_sales.csv", x=0.02, ha="left",
                 fontsize=15, fontweight="bold", color=vc.CHROME["primary_ink"])
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out_path = os.path.join(OUT_DIR, "coffee_sales.png")
    fig.savefig(out_path, dpi=150)
    print(f"Wrote {out_path} (top region: {top_region})")


if __name__ == "__main__":
    main()
