"""Generate a fake cholesterol clinical-trial dataset.

Reproducible (fixed seed). Writes data/cholesterol_trial.csv.

Each row is one patient in a 12-week trial. Three active pills and a
placebo. We also record weekly exercise minutes and whether the patient
followed a fat-free diet, because both also affect cholesterol.

    python examples/generate_trial_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "cholesterol_trial.csv"

# Average mg/dL cholesterol drop attributable to each arm (before exercise/diet).
ARM_EFFECT = {
    "Lipitor": 52,    # strongest statin in this trial
    "Crestor": 41,
    "Zocor": 28,
    "Placebo": 4,     # near-zero, the control
}
PER_ARM = 45  # patients per arm


def main() -> None:
    rng = np.random.default_rng(42)
    rows = []
    pid = 1000
    for arm, effect in ARM_EFFECT.items():
        for _ in range(PER_ARM):
            pid += 1
            baseline = float(rng.normal(245, 22))              # starting cholesterol
            exercise = max(0.0, float(rng.normal(110, 55)))    # minutes/week
            fat_free = bool(rng.random() < 0.45)               # on the diet?
            # Reduction = drug effect + exercise benefit + diet benefit + noise.
            reduction = (
                effect
                + 0.06 * exercise
                + (9 if fat_free else 0)
                + float(rng.normal(0, 7))
            )
            reduction = max(0.0, reduction)                    # can't go up on average
            final = baseline - reduction
            rows.append(
                {
                    "patient_id": pid,
                    "treatment": arm,
                    "baseline_cholesterol": round(baseline, 1),
                    "final_cholesterol": round(final, 1),
                    "cholesterol_reduction": round(reduction, 1),
                    "exercise_minutes": round(exercise, 1),
                    "fat_free_diet": "Yes" if fat_free else "No",
                }
            )

    df = pd.DataFrame(rows)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {len(df)} rows to {OUT}")


if __name__ == "__main__":
    main()
