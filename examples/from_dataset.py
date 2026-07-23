"""Build one of each chart type straight from the bundled sample datasets."""

import os

import matplotlib.pyplot as plt

import viscomm as vc
from viscomm import datasets
from viscomm.theme import CHROME

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(CHROME["surface"])

    d = datasets.monthly_active_users()
    vc.line(d.x, series=d.series, title=d.title, ylabel=d.ylabel, ax=axes[0, 0])

    d = datasets.quarterly_revenue_by_region()
    vc.bar(d.categories, series=d.series, title=d.title, subtitle=d.subtitle,
           ylabel=d.ylabel, ax=axes[0, 1])

    d = datasets.spend_vs_signups()
    vc.scatter(None, None, series=d.series, title=d.title,
               xlabel=d.xlabel, ylabel=d.ylabel, ax=axes[1, 0])

    d = datasets.traffic_by_channel()
    vc.pie(d.labels, d.values, title=d.title, ax=axes[1, 1])

    fig.suptitle("Brewhaus sample datasets", x=0.02, ha="left",
                 fontsize=15, fontweight="bold", color=CHROME["primary_ink"])
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_path = os.path.join(OUT_DIR, "from_dataset.png")
    fig.savefig(out_path, dpi=150)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
