"""Ready-to-plot sample datasets for building visuals with viscomm.

All data is synthetic but realistic, and fully deterministic (fixed random
seeds), so every call and the exported CSVs always match. The theme is a
fictional specialty-coffee company, "Brewhaus".

Each loader returns a small namedtuple whose fields line up with a chart
function's arguments, plus a suggested title/labels, so plotting is a
one-liner:

    from viscomm import datasets
    import viscomm as vc

    d = datasets.monthly_active_users()
    vc.line(d.x, series=d.series, title=d.title, ylabel=d.ylabel)

Call `datasets.export_csv("data")` (or run examples/generate_data.py) to
write every dataset out as a tidy CSV.
"""

import csv
import os
from collections import namedtuple

import numpy as np

LineData = namedtuple("LineData", "x series title ylabel")
BarData = namedtuple("BarData", "categories series title subtitle ylabel")
ScatterData = namedtuple("ScatterData", "series title xlabel ylabel")
PieData = namedtuple("PieData", "labels values title")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def monthly_active_users():
    """Line chart: monthly active users (thousands) by platform, 2025.

    Three platforms trending up at different rates, with mild noise.
    """
    rng = np.random.default_rng(1)
    x = list(MONTHS)
    series = {}
    for name, start, growth in [("Mobile", 42, 3.1), ("Web", 55, 1.2), ("Kiosk", 12, 0.6)]:
        trend = start + growth * np.arange(12)
        noise = rng.normal(0, growth * 0.4, 12)
        series[name] = [round(v, 1) for v in trend + noise]
    return LineData(x=x, series=series, title="Monthly active users by platform",
                    ylabel="Users (K)")


def quarterly_revenue_by_region():
    """Bar chart: revenue ($M) by region, grouped by year (2024 vs 2025)."""
    rng = np.random.default_rng(2)
    regions = ["North", "South", "East", "West"]
    base = np.array([18.0, 12.5, 22.0, 9.5])
    y2024 = [round(v, 1) for v in base + rng.normal(0, 1.0, 4)]
    y2025 = [round(v, 1) for v in base * 1.15 + rng.normal(0, 1.0, 4)]
    return BarData(categories=regions, series={"2024": y2024, "2025": y2025},
                   title="Revenue by region", subtitle="$ millions", ylabel="$M")


def spend_vs_signups():
    """Scatter: marketing spend ($K) vs new signups, by channel.

    Three channels (scatter's supported maximum), each with its own
    spend-to-signup efficiency, over a set of weekly campaigns.
    """
    rng = np.random.default_rng(3)
    series = {}
    for name, eff, n in [("Paid search", 6.5, 14), ("Social", 4.2, 14), ("Email", 9.0, 12)]:
        spend = np.sort(rng.uniform(2, 20, n))
        signups = spend * eff + rng.normal(0, 8, n)
        series[name] = ([round(v, 1) for v in spend],
                        [max(0, round(v)) for v in signups])
    return ScatterData(series=series, title="Marketing spend vs. signups",
                       xlabel="Spend ($K)", ylabel="New signups")


def traffic_by_channel():
    """Pie: share of site traffic by acquisition channel."""
    labels = ["Direct", "Organic", "Referral", "Paid", "Email"]
    values = [34, 28, 16, 14, 8]
    return PieData(labels=labels, values=values, title="Traffic by channel")


ALL_LOADERS = {
    "monthly_active_users": monthly_active_users,
    "quarterly_revenue_by_region": quarterly_revenue_by_region,
    "spend_vs_signups": spend_vs_signups,
    "traffic_by_channel": traffic_by_channel,
}


def export_csv(out_dir):
    """Write every dataset to a tidy CSV in `out_dir`. Returns the paths."""
    os.makedirs(out_dir, exist_ok=True)
    paths = {}

    def _write(name, header, rows):
        path = os.path.join(out_dir, name + ".csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
        paths[name] = path

    d = monthly_active_users()
    _write("monthly_active_users", ["month", *d.series],
           [[m, *(d.series[s][i] for s in d.series)] for i, m in enumerate(d.x)])

    d = quarterly_revenue_by_region()
    _write("quarterly_revenue_by_region", ["region", *d.series],
           [[c, *(d.series[s][i] for s in d.series)] for i, c in enumerate(d.categories)])

    d = spend_vs_signups()
    rows = []
    for channel, (spend, signups) in d.series.items():
        rows.extend([channel, s, u] for s, u in zip(spend, signups))
    _write("spend_vs_signups", ["channel", "spend_k", "signups"], rows)

    d = traffic_by_channel()
    _write("traffic_by_channel", ["channel", "share_pct"],
           list(zip(d.labels, d.values)))

    return paths
