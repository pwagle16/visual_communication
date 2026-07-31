"""Write a small, tidy sample dataset to data/coffee_sales.csv.

Deterministic (fixed seed) so the file is reproducible. It models a
fictional coffee company's monthly performance across four regions --
one file rich enough to exercise every viscomm chart type:

    month, region, revenue_k, orders, ad_spend_k
"""

import csv
import os
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Each region: (baseline revenue $K in Jan, monthly growth $K, seasonal swing $K)
REGIONS = {
    "North": (42, 1.8, 6),
    "South": (30, 2.6, 4),
    "East": (25, 1.1, 5),
    "West": (18, 3.0, 3),
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    rng = random.Random(7)  # fixed seed -> identical file every run
    path = os.path.join(DATA_DIR, "coffee_sales.csv")

    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["month", "region", "revenue_k", "orders", "ad_spend_k"])
        for region, (base, growth, swing) in REGIONS.items():
            for i, month in enumerate(MONTHS):
                # Trend + a summer (mid-year) seasonal bump + a little noise.
                seasonal = swing * (1 - ((i - 6) / 6) ** 2)
                revenue = base + growth * i + seasonal + rng.uniform(-2, 2)
                revenue = round(max(revenue, 1), 1)
                orders = int(revenue * rng.uniform(11, 14))  # ~$/order varies a bit
                ad_spend = round(revenue * rng.uniform(0.10, 0.18), 1)
                writer.writerow([month, region, revenue, orders, ad_spend])

    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
