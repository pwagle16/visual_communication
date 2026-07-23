"""Write every sample dataset out as a tidy CSV under data/."""

import os

from viscomm import datasets

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def main():
    paths = datasets.export_csv(DATA_DIR)
    print(f"Wrote {len(paths)} datasets to {DATA_DIR}:")
    for name, path in paths.items():
        print(f"  - {os.path.basename(path)}")


if __name__ == "__main__":
    main()
