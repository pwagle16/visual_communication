"""Generates one sample PNG per chart type into examples/output/."""

import os

import viscomm as vc

OUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ax = vc.bar(
        ["Q1", "Q2", "Q3", "Q4"],
        series={"2024": [12, 18, 14, 22], "2025": [15, 20, 19, 27]},
        title="Quarterly revenue",
        subtitle="$ millions",
        ylabel="$M",
    )
    ax.figure.savefig(os.path.join(OUT_DIR, "bar.png"), dpi=150)

    ax = vc.line(
        list(range(2019, 2026)),
        series={
            "North": [10, 12, 15, 14, 18, 22, 25],
            "South": [8, 9, 11, 13, 12, 14, 16],
        },
        title="Active users by region",
        ylabel="Users (K)",
    )
    ax.figure.savefig(os.path.join(OUT_DIR, "line.png"), dpi=150)

    ax = vc.scatter(
        None,
        None,
        series={
            "Group A": ([1, 2, 3, 4, 5], [2, 3, 2.5, 4, 5]),
            "Group B": ([2, 3, 4, 5, 6], [5, 4, 6, 5, 7]),
        },
        title="Height vs. weight",
        xlabel="Height (cm, centered)",
        ylabel="Weight (kg, centered)",
    )
    ax.figure.savefig(os.path.join(OUT_DIR, "scatter.png"), dpi=150)

    ax = vc.pie(
        ["Direct", "Organic search", "Referral", "Paid"],
        [35, 30, 20, 15],
        title="Traffic by channel",
    )
    ax.figure.savefig(os.path.join(OUT_DIR, "pie.png"), dpi=150)

    print(f"Wrote sample charts to {OUT_DIR}")


if __name__ == "__main__":
    main()
