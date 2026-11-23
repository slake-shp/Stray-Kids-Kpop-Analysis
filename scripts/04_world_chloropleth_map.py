import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from pathlib import Path
from shapely.geometry import Point
from matplotlib.patches import Patch

# =====================================
# Load Data
# =====================================

print("Loading datasets...")

world = gpd.read_file(
    "data/boundaries/natural_earth/ne_50m_admin_0_countries.shp"
)

stats = pd.read_csv(
    "data/processed/stray_kids_country_stats.csv"
)

# =====================================
# Validation
# =====================================

assert len(world) > 0
assert len(stats) > 0

assert "iso3" in stats.columns
assert "stray_kids_market_strength" in stats.columns

print("✓ Input datasets validated")

# =====================================
# Market Classification
# =====================================

stats["market_category"] = pd.cut(
    stats["stray_kids_market_strength"],
    bins=[0, 5, 10, 15, 25],
    labels=[
        "Emerging Market",
        "Growth Market",
        "Established Market",
        "Core Market"
    ]
)

# =====================================
# Join Data
# =====================================

world = world.merge(
    stats,
    left_on="ADM0_A3",
    right_on="iso3",
    how="left"
)

matched = world[
    world["stray_kids_market_strength"]
    .notna()
]

print(
    f"Matched countries: {len(matched)}"
)

assert len(matched) == 13

print("✓ Country join successful")

# =====================================
# Projection
# =====================================

world = world.to_crs(
    "ESRI:54030"
)

print(
    "✓ Robinson projection applied"
)

# =====================================
# Seoul Origin Point
# =====================================

seoul = gpd.GeoDataFrame(
    {"name": ["Seoul"]},
    geometry=[
        Point(
            126.9780,
            37.5665
        )
    ],
    crs="EPSG:4326"
)

seoul = seoul.to_crs(
    world.crs
)

print(
    "✓ Seoul origin point created"
)

# =====================================
# Colour Palette
# =====================================

market_colours = {
    "Core Market": "#2E7D32",         # Forest Green
    "Established Market": "#7CB342", # Olive Green
    "Growth Market": "#D4A017",      # Muted Gold
    "Emerging Market": "#C26A5A"     # Terracotta
}

world["colour"] = (
    world["market_category"]
    .map(market_colours)
)

# =====================================
# Create Figure
# =====================================

fig, ax = plt.subplots(
    figsize=(18, 10)
)

fig.patch.set_facecolor(
    "white"
)

ax.set_facecolor(
    "#F6FAFC"
)

# =====================================
# Base Countries
# =====================================

world.plot(
    color="#E6E6E6",
    linewidth=0.2,
    edgecolor="white",
    ax=ax
)

# =====================================
# Classified Markets
# =====================================

classified = world.dropna(
    subset=["market_category"]
)

classified.plot(
    color=classified["colour"],
    linewidth=0.6,
    edgecolor="black",
    ax=ax
)

# =====================================
# Seoul Marker
# =====================================

seoul.plot(
    ax=ax,
    color="#1565C0",
    markersize=120,
    edgecolor="white",
    linewidth=1,
    zorder=10
)

x, y = (
    seoul.geometry.iloc[0]
    .coords[0]
)

ax.annotate(
    "Seoul\n(K-Pop Origin)",
    xy=(x, y),
    xytext=(-90, 25),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold",
    color="#1565C0",
    ha="right",
    arrowprops=dict(
        arrowstyle="-",
        color="#1565C0",
        lw=1.5
    ),
    bbox=dict(
        facecolor="white",
        alpha=0.95,
        edgecolor="#1565C0",
        boxstyle="round,pad=0.3"
    )
)

# =====================================
# North Arrow
# =====================================

ax.annotate(
    "",
    xy=(0.93, 0.92),
    xytext=(0.93, 0.82),
    xycoords=ax.transAxes,
    arrowprops=dict(
        facecolor="black",
        edgecolor="black",
        width=3,
        headwidth=12
    )
)

ax.text(
    0.93,
    0.94,
    "N",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=16,
    fontweight="bold"
)

# =====================================
# Market Callouts
# =====================================

callout_countries = [
    "Australia",
    "Canada",
    "South Korea"
]

offsets = {
    "Australia": (50, -15),
    "Canada": (40, 25),
    "South Korea": (-95, -40)
}

for country in callout_countries:

    row = world[
        world["NAME"] == country
    ]

    if row.empty:
        continue

    value = round(
        float(
            row[
                "stray_kids_market_strength"
            ].iloc[0]
        ),
        2
    )

    centroid = (
        row.geometry
        .centroid
        .iloc[0]
    )

    dx, dy = offsets[country]

    ax.annotate(
        (
            f"{country}\n"
            f"Score: {value}"
        ),
        xy=(
            centroid.x,
            centroid.y
        ),
        xytext=(dx, dy),
        textcoords="offset points",
        fontsize=9,
        bbox=dict(
            facecolor="white",
            alpha=0.95,
            edgecolor="#666666",
            boxstyle="round,pad=0.4"
        ),
        arrowprops=dict(
            arrowstyle="-",
            color="#666666",
            lw=1
        )
    )

# =====================================
# Legend
# =====================================

legend_items = [

    Patch(
        facecolor="#2E7D32",
        label="Core Market"
    ),

    Patch(
        facecolor="#7CB342",
        label="Established Market"
    ),

    Patch(
        facecolor="#D4A017",
        label="Growth Market"
    ),

    Patch(
        facecolor="#C26A5A",
        label="Emerging Market"
    )

]

ax.legend(
    handles=legend_items,
    title="Market Classification",
    loc="lower left",
    frameon=True
)

# =====================================
# Title
# =====================================

ax.set_title(
    (
        "Global Diffusion of Stray Kids\n"
        "Population-Normalised Market Strength by Country"
    ),
    fontsize=20,
    fontweight="bold",
    pad=20
)

# =====================================
# Top Market Ranking Table
# =====================================

top_markets = (
    stats[
        [
            "country",
            "market_category",
            "stray_kids_market_strength"
        ]
    ]
    .sort_values(
        "stray_kids_market_strength",
        ascending=False
    )
    .head(5)
)

table_lines = []

table_lines.append(
    "TOP MARKETS"
)

table_lines.append(
    "Stray Kids Market Strength"
)

table_lines.append(
    "(Using Last.fm Rankings and"
)

table_lines.append(
    "World Bank Population Data)"
)

table_lines.append(
    ""
)

table_lines.append(
    "Rank Country        Score"
)

table_lines.append(
    "──────────────────────────"
)

for i, row in enumerate(
    top_markets.itertuples(),
    start=1
):

    country = row.country

    score = (
        f"{row.stray_kids_market_strength:.2f}"
    )

    line = (
        f"{i:<2}   "
        f"{country:<14} "
        f"{score:>5}"
    )

    table_lines.append(line)

table_text = "\n".join(
    table_lines
)

ax.text(
    0.965,
    0.76,
    table_text,
    transform=ax.transAxes,
    ha="right",
    va="top",
    family="monospace",
    fontsize=9,
    bbox=dict(
        facecolor="white",
        edgecolor="#666666",
        alpha=0.97,
        boxstyle="round,pad=0.7"
    )
)

# =====================================
# Source Note
# =====================================

plt.figtext(
    0.01,
    0.015,
    (
        "Sources: Last.fm API | "
        "World Bank Population Data | "
        "Natural Earth Admin 0 Countries"
    ),
    fontsize=8
)

# =====================================
# Projection Note
# =====================================

plt.figtext(
    0.99,
    0.015,
    "Projection: Robinson (ESRI:54030)",
    fontsize=8,
    ha="right"
)

# =====================================
# Layout
# =====================================

ax.set_axis_off()

plt.tight_layout()

# =====================================
# Export
# =====================================

Path(
    "maps/final"
).mkdir(
    parents=True,
    exist_ok=True
)

output = (
    "maps/final/"
    "stray_kids_market_strength_world.png"
)

plt.savefig(
    output,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\n✓ Map exported successfully"
)

print(
    f"\nOutput:\n{output}"
)