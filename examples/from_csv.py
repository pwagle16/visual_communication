"""Load data/coffee_sales.csv and render a coffee-themed two-chart figure.

Reads with the standard-library csv module (viscomm takes plain lists, so
no pandas needed). Renders monthly revenue lines per region alongside a
total-revenue bar chart, using a soft brown pastel palette -- with the
highest-revenue region drawn in dark brown to make it stand out. Colors are
mapped per region, so a region keeps the same color across both charts.

For fun, the whole figure is dressed up as coffee: a latte-cream page,
coffee-brown chrome, and little hand-drawn coffee beans scattered around
the margins. All of that decoration lives here in the example -- the
viscomm library itself stays plain.
"""

import csv
import os
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

import viscomm as vc

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(os.path.dirname(HERE), "data", "coffee_sales.csv")
OUT_DIR = os.path.join(HERE, "output")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# --- coffee palette ---------------------------------------------------------
PAGE = "#e7d7bf"       # latte-cream page background
PANEL = "#f4ecdd"      # lighter foam for the chart panels
COFFEE_INK = "#2e1c0d"  # espresso-dark text (titles)
DESC_INK = "#5f4025"    # readable roast brown (descriptions)
GRID = "#dcc9ab"       # muted crema gridlines
SPINE = "#9c7b56"      # roasted-tan axis lines

BROWN_PASTEL = ["#cdb391", "#c2a279", "#dac7a8", "#b89b74"]  # also-ran regions
DARK_BROWN = "#4a2f1a"                                       # the leader
BEAN_ROASTS = ["#3d2415", "#4a2f1a", "#5b3a22", "#33200f"]   # bean fill variety
BEAN_EDGE = "#20120a"
BEAN_SEAM = "#c8a877"

FIG_W, FIG_H = 16, 6  # inches; used to keep beans round despite the wide frame


def draw_bean(deco, fx, fy, size, angle, fill):
    """Draw one coffee bean (ellipse + curved seam) centered at figure
    fraction (fx, fy). `size` is the half-length in inches; dividing pixel
    offsets by the figure's inch extents keeps the bean shape from stretching."""
    ang = np.radians(angle)
    ca, sa = np.cos(ang), np.sin(ang)
    t = np.linspace(0, 2 * np.pi, 48)
    ox, oy = np.cos(t) * size, np.sin(t) * size * 0.6
    deco.fill(fx + (ox * ca - oy * sa) / FIG_W, fy + (ox * sa + oy * ca) / FIG_H,
              facecolor=fill, edgecolor=BEAN_EDGE, linewidth=1.1, zorder=5)
    s = np.linspace(-0.8, 0.8, 24)
    sx, sy = s * size, np.sin(s * np.pi) * 0.12 * size  # gentle bow for the crease
    deco.plot(fx + (sx * ca - sy * sa) / FIG_W, fy + (sx * sa + sy * ca) / FIG_H,
              color=BEAN_SEAM, linewidth=1.3, zorder=6, solid_capstyle="round")


def scatter_beans(fig, rng):
    """Overlay a transparent full-figure axes and sprinkle beans in the margins."""
    deco = fig.add_axes((0, 0, 1, 1), zorder=4)
    deco.set_axis_off()
    deco.set_xlim(0, 1)
    deco.set_ylim(0, 1)
    deco.patch.set_alpha(0)

    spots = []
    for cx, cy in [(0.03, 0.08), (0.03, 0.9), (0.97, 0.08), (0.97, 0.9)]:  # corners
        spots += [(cx + rng.uniform(-0.025, 0.025), cy + rng.uniform(-0.07, 0.07))
                  for _ in range(4)]
    spots += [(rng.uniform(0.72, 0.92), rng.uniform(0.9, 0.97)) for _ in range(3)]  # top-right
    spots += [(rng.uniform(0.08, 0.28), rng.uniform(0.9, 0.97)) for _ in range(3)]  # top-left
    spots += [(rng.uniform(0.005, 0.035), rng.uniform(0.25, 0.75)) for _ in range(4)]  # left
    spots += [(rng.uniform(0.95, 0.99), rng.uniform(0.25, 0.75)) for _ in range(4)]  # right

    for fx, fy in spots:
        draw_bean(deco, min(max(fx, 0.01), 0.99), min(max(fy, 0.02), 0.98),
                  size=rng.uniform(0.20, 0.32), angle=rng.uniform(0, 360),
                  fill=rng.choice(BEAN_ROASTS))


def brew(ax):
    """Recolor a finished chart's chrome into warm coffee tones and make its
    title + description read clearly against the busy background."""
    ax.set_facecolor(PANEL)
    for gl in ax.get_xgridlines() + ax.get_ygridlines():
        gl.set_color(GRID)
    for name, spine in ax.spines.items():
        if spine.get_visible():
            spine.set_color(SPINE)

    # viscomm draws the title then the subtitle last, as the final two texts
    # on the axes -- darken and enlarge them so both stand out clearly.
    if len(ax.texts) >= 2:
        title_txt, desc_txt = ax.texts[-2], ax.texts[-1]
        title_txt.set(color=COFFEE_INK, fontsize=16, fontweight="bold")
        desc_txt.set(color=DESC_INK, fontsize=11.5)

    legend = ax.get_legend()
    if legend:
        for t in legend.get_texts():
            t.set_color(DESC_INK)


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

    # One color per region: dark brown for the leader, pastels for the rest,
    # built in `regions` order so it lines up with both charts.
    pastels = iter(BROWN_PASTEL)
    region_color = {
        reg: DARK_BROWN if reg == top_region else next(pastels) for reg in regions
    }
    colors = [region_color[reg] for reg in regions]

    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(PAGE)

    vc.line(list(range(1, 13)), series=revenue_series, colors=colors,
            title="Monthly revenue by region",
            subtitle="Revenue ($K) each month, Jan-Dec -- one line per region",
            xlabel="Month", ylabel="$K", ax=axes[0])
    vc.bar(regions, values=[totals[r] for r in regions], colors=colors,
           title="Total revenue by region",
           subtitle=f"Full-year revenue ($K) per region -- {top_region} earns the most",
           ylabel="$K", ax=axes[1])

    for ax in axes:
        brew(ax)

    # A clear dashboard header: bold title + a one-line description of the figure.
    fig.text(0.5, 0.935, "☕  Coffee Sales Dashboard", ha="center",
             fontsize=23, fontweight="bold", color=COFFEE_INK)
    fig.text(0.5, 0.865, "Monthly revenue trends and full-year totals across four "
             "regions -- North leads.", ha="center", fontsize=13, color=DESC_INK)
    fig.subplots_adjust(left=0.07, right=0.93, top=0.72, bottom=0.20, wspace=0.22)
    scatter_beans(fig, random.Random(11))

    out_path = os.path.join(OUT_DIR, "coffee_sales.png")
    fig.savefig(out_path, dpi=150, facecolor=PAGE)
    print(f"Wrote {out_path} (top region: {top_region})")
    plt.show()  # pop the chart open in a window when run interactively


if __name__ == "__main__":
    main()
