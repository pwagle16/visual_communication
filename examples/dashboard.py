"""Composes all four chart types into a single 2x2 dashboard figure.

Every viscomm chart function accepts an `ax=` argument, so composing them
onto a shared figure is just matplotlib's normal subplot grid -- no special
"dashboard" API needed.
"""

import os

import matplotlib.pyplot as plt

import viscomm as vc
from viscomm.theme import CHROME

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(CHROME["surface"])

    vc.bar(
        ["Q1", "Q2", "Q3", "Q4"],
        series={"2024": [12, 18, 14, 22], "2025": [15, 20, 19, 27]},
        title="Quarterly revenue",
        subtitle="$ millions",
        ylabel="$M",
        ax=axes[0, 0],
    )

    vc.line(
        list(range(2019, 2026)),
        series={
            "North": [10, 12, 15, 14, 18, 22, 25],
            "South": [8, 9, 11, 13, 12, 14, 16],
        },
        title="Active users by region",
        ylabel="Users (K)",
        ax=axes[0, 1],
    )

    vc.scatter(
        None,
        None,
        series={
            "Group A": ([1, 2, 3, 4, 5], [2, 3, 2.5, 4, 5]),
            "Group B": ([2, 3, 4, 5, 6], [5, 4, 6, 5, 7]),
        },
        title="Height vs. weight",
        xlabel="Height (cm, centered)",
        ylabel="Weight (kg, centered)",
        ax=axes[1, 0],
    )

    vc.pie(
        ["Direct", "Organic search", "Referral", "Paid"],
        [35, 30, 20, 15],
        title="Traffic by channel",
        ax=axes[1, 1],
    )

    fig.suptitle("viscomm -- all chart types", x=0.02, ha="left", fontsize=15, fontweight="bold", color=CHROME["primary_ink"])
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out_path = os.path.join(OUT_DIR, "dashboard.png")
    fig.savefig(out_path, dpi=150)
    print(f"Wrote combined dashboard to {out_path}")


if __name__ == "__main__":
    main()
