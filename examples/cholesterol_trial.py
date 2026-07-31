"""Visualize the fake cholesterol trial with a mix of chart types.

    python examples/generate_trial_data.py   # once, to create the data
    python examples/cholesterol_trial.py      # then this

Writes charts to examples/output/trial/.
"""

from pathlib import Path

import pandas as pd

import simple_eda as eda

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cholesterol_trial.csv"
OUT = ROOT / "examples" / "output" / "trial"


def main() -> None:
    df = pd.read_csv(DATA)
    OUT.mkdir(parents=True, exist_ok=True)
    S = "clinical"  # calm hospital palette

    # Which pill decreased cholesterol the most? Spotlight the winner; the
    # placebo and the rest recede so the result reads at a glance.
    print(eda.plot_bar(df, "treatment", "cholesterol_reduction",
                       path=str(OUT / "rank.png"), style=S, highlight="Lipitor"))
    # Full spread per treatment, not just the average.
    print(eda.plot_box(df, "treatment", "cholesterol_reduction", str(OUT / "box.png"), style=S))
    # Fat-free diet effect within each treatment arm.
    print(eda.plot_bar(df, "treatment", "cholesterol_reduction",
                       group="fat_free_diet", path=str(OUT / "diet.png"), style=S))
    # More exercise -> bigger drop?
    print(eda.plot_scatter(df, "exercise_minutes", "cholesterol_reduction",
                          str(OUT / "exercise.png"), style=S))
    # Distribution of the outcome, and how the numeric drivers relate.
    print(eda.plot_histogram(df, "cholesterol_reduction", str(OUT / "hist.png"), style=S))
    print(eda.plot_correlation(df, str(OUT / "corr.png"), style=S))


if __name__ == "__main__":
    main()
