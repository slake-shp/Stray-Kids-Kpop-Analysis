# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

import os
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib import rcParams

from shapely.affinity import translate, scale
from matplotlib.patches import Circle

# --------------------------------------------------
# GLOBAL FONT
# --------------------------------------------------

rcParams["font.family"] = "sans-serif"

rcParams["font.sans-serif"] = [
    "Trebuchet MS",
    "Arial",
    "DejaVu Sans"
]

rcParams["font.size"] = 10

# --------------------------------------------------
# OUTPUT DIRECTORY
# --------------------------------------------------

os.makedirs("maps/final", exist_ok=True)

# --------------------------------------------------
# READ CSV FOR INSPECTION
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/stray_kids_country_stats.csv"
)

print(df.columns)

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

COUNTRIES = (
    "data/boundaries/natural_earth/"
    "ne_50m_admin_0_countries.shp"
)

MARKETS = (
    "data/processed/"
    "stray_kids_country_stats.csv"
)

OUTPUT = (
    "maps/final/stray_kids_orbital_system.png"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

world = gpd.read_file(COUNTRIES)
markets = pd.read_csv(MARKETS)

print(f"Countries: {len(world)}")
print(f"Market records: {len(markets)}")

# --------------------------------------------------
# JOIN
# --------------------------------------------------

gdf = world.merge(
    markets,
    left_on="ADM0_A3",
    right_on="iso3",
    how="inner"
)

print(f"Joined countries: {len(gdf)}")

# --------------------------------------------------
# PROJECT CRS
# --------------------------------------------------

gdf = gdf.to_crs("EPSG:3857")

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

print("\nMatched countries:")

print(
    gdf[
        ["country", "iso3", "stray_kids_market_strength"]
    ].sort_values(
        "stray_kids_market_strength",
        ascending=False
    )
)

print("\nAvailable columns after join:")

print(gdf.columns.tolist())

# --------------------------------------------------
# SORT BY MARKET STRENGTH
# --------------------------------------------------

gdf = gdf.sort_values(
    "stray_kids_market_strength",
    ascending=False
).reset_index(drop=True)

# --------------------------------------------------
# REMOVE SOUTH KOREA
# SEOUL REPRESENTS THE CENTRE
# --------------------------------------------------

gdf = gdf[
    gdf["iso3"] != "KOR"
].copy()

print(
    gdf["CONTINENT"]
    .value_counts()
)

gdf = gdf.reset_index(drop=True)

gdf["rank"] = np.arange(
    1,
    len(gdf) + 1
)

# --------------------------------------------------
# ORBITAL DISTANCE
# --------------------------------------------------

def get_orbit(rank):

    if rank <= 3:
        return 18_000_000

    elif rank <= 7:
        return 36_000_000

    else:
        return 54_000_000

gdf["orbit_radius"] = gdf["rank"].apply(
    get_orbit
)

# --------------------------------------------------
# CONTINENTAL ORBITAL SECTORS
# --------------------------------------------------

sector_ranges = {
    "Oceania": (70, 110),
    "Europe": (160, 200),
    "Asia": (300, 20),
    "North America": (240, 285),
    "South America": (210, 230)
}

angles = []

for continent, group in gdf.groupby("CONTINENT"):

    if continent not in sector_ranges:
        continue

    start_deg, end_deg = sector_ranges[continent]

    # Handle sectors crossing 360°
    if start_deg > end_deg:

        sector_angles = np.linspace(
            np.deg2rad(start_deg),
            np.deg2rad(end_deg + 360),
            len(group)
        )

        sector_angles = np.mod(
            sector_angles,
            2 * np.pi
        )

    else:

        sector_angles = np.linspace(
            np.deg2rad(start_deg),
            np.deg2rad(end_deg),
            len(group)
        )

    for idx, angle in zip(group.index, sector_angles):
        angles.append((idx, angle))

angle_lookup = dict(angles)

gdf["angle"] = gdf.index.map(angle_lookup)

print(
    gdf[
        ["country", "CONTINENT", "rank", "orbit_radius"]
    ]
)

# --------------------------------------------------
# ORBIT DEBUG
# --------------------------------------------------

debug_df = gdf[
    [
        "country",
        "CONTINENT",
        "rank",
        "orbit_radius",
        "angle"
    ]
].copy()

debug_df["angle_deg"] = np.degrees(
    debug_df["angle"]
)

print("\nOrbit assignments:")
print(
    debug_df[
        [
            "country",
            "CONTINENT",
            "rank",
            "orbit_radius",
            "angle_deg"
        ]
    ].sort_values("rank")
)

# --------------------------------------------------
# SEOUL
# --------------------------------------------------

SEOUL_X = 0
SEOUL_Y = 0

# --------------------------------------------------
# ORBITAL COORDINATES
# --------------------------------------------------

gdf["orbit_x"] = (
    SEOUL_X +
    gdf["orbit_radius"] *
    np.cos(gdf["angle"])
)

gdf["orbit_y"] = (
    SEOUL_Y +
    gdf["orbit_radius"] *
    np.sin(gdf["angle"])
)

# --------------------------------------------------
# COUNTRY SIZE SCALING
# NORMALISE COUNTRY AREA
# --------------------------------------------------

gdf["country_area"] = gdf.geometry.area

median_area = gdf["country_area"].median()

gdf["size_factor"] = np.sqrt(
    median_area / gdf["country_area"]
)

gdf["size_factor"] = gdf["size_factor"].clip(
    lower=0.50,
    upper=2.00
)

# --------------------------------------------------
# MOVE COUNTRIES TO ORBITS
# --------------------------------------------------

new_geometries = []

for _, row in gdf.iterrows():

    geom = row.geometry

    cx = geom.centroid.x
    cy = geom.centroid.y

    geom = scale(
        geom,
        xfact=row.size_factor,
        yfact=row.size_factor,
        origin="centroid"
    )

    dx = row.orbit_x - cx
    dy = row.orbit_y - cy

    geom = translate(
        geom,
        xoff=dx,
        yoff=dy
    )

    new_geometries.append(geom)

gdf["geometry"] = new_geometries

# --------------------------------------------------
# FIGURE
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(16, 16)
)

space_colour = "#050816"

fig.patch.set_facecolor(
    space_colour
)

ax.set_facecolor(
    space_colour
)

# --------------------------------------------------
# ORBIT RINGS
# --------------------------------------------------

for radius in [
    18_000_000,
    36_000_000,
    54_000_000
]:

    orbit = Circle(
        (0, 0),
        radius,
        fill=False,
        linestyle="--",
        linewidth=1.5,
        edgecolor="white",
        alpha=0.25
    )

    ax.add_patch(orbit)

# --------------------------------------------------
# STAR FIELD
# --------------------------------------------------

np.random.seed(42)

n_stars = 1500

ax.scatter(
    np.random.uniform(
        -65_000_000,
        65_000_000,
        n_stars
    ),
    np.random.uniform(
        -65_000_000,
        65_000_000,
        n_stars
    ),
    s=np.random.uniform(
        1,
        6,
        n_stars
    ),
    color="white",
    alpha=0.5,
    zorder=0
)

# --------------------------------------------------
# PLOT COUNTRIES
# --------------------------------------------------

# Glow layer to stand out more

gdf.plot(
    color="#9C6BFF",
    linewidth=0,
    alpha=0.25,
    ax=ax,
    zorder=5
)

plot = gdf.plot(
    column="stray_kids_market_strength",
    cmap="plasma",
    linewidth=1.2,
    edgecolor="white",
    legend=False,
    ax=ax,
    zorder=10
)

# --------------------------------------------------
# MARKET STRENGTH LEGEND
# --------------------------------------------------

norm = Normalize(
    vmin=gdf["stray_kids_market_strength"].min(),
    vmax=gdf["stray_kids_market_strength"].max()
)

sm = ScalarMappable(
    cmap="plasma",
    norm=norm
)

sm.set_array([])

cax = fig.add_axes(
    [0.91, 0.06, 0.018, 0.16]
)

cbar = fig.colorbar(
    sm,
    cax=cax
)

cbar.set_label(
    "Market Strength",
    color="white",
    fontsize=10
)

plt.setp(
    cbar.ax.get_yticklabels(),
    color="white"
)

cbar.outline.set_edgecolor("white")

cbar.ax.set_facecolor("#050816")

# --------------------------------------------------
# LABELS
# --------------------------------------------------

for _, row in gdf.iterrows():

    c = row.geometry.centroid

    if row["rank"] <= 3:
        label_size = 14
        label_offset = 3_500_000

    elif row["rank"] <= 7:
        label_size = 11
        label_offset = 2_500_000

    else:
        label_size = 9
        label_offset = 2_000_000

    ax.text(
        c.x,
        c.y + label_offset,
        row["country"],
        fontsize=label_size,
        fontweight="bold",
        color="white",
        ha="center",
        va="bottom",
        bbox=dict(
            facecolor="black",
            edgecolor="white",
            linewidth=0.4,
            alpha=0.85,
            pad=2
        ),
        zorder=20
    )

# --------------------------------------------------
# STRAY KIDS LOGO
# --------------------------------------------------

# Halo 1

ax.scatter(
    0,
    0,
    s=35000,
    color="#8A2BE2",
    alpha=0.06,
    zorder=90
)

# Halo 2

ax.scatter(
    0,
    0,
    s=22000,
    color="#FFFFFF",
    alpha=0.04,
    zorder=91
)

# Halo 3

ax.scatter(
    0,
    0,
    s=12000,
    color="#FFD700",
    alpha=0.05,
    zorder=92
)

# Load logo

logo = mpimg.imread(
    "data/images/Stray_Kids_Symbol.webp"
)

# Create image box

imagebox = OffsetImage(
    logo,
    zoom=0.20
)

# Place logo in centre

ab = AnnotationBbox(
    imagebox,
    (0, 0),
    frameon=False,
    zorder=100
)

ax.add_artist(ab)

# Label

ax.text(
    0,
    -8_000_000,
    "STRAY KIDS",
    fontsize=18,
    fontweight="bold",
    color="white",
    ha="center",
    va="top",
    bbox=dict(
        facecolor="black",
        edgecolor="white",
        linewidth=0.5,
        alpha=0.85,
        pad=2
    ),
    zorder=101
)

print("Logo shape:", logo.shape)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

ax.set_title(
    (
        "THE STRAY KIDS SYSTEM\n"
        "Countries Positioned by Relative Last.fm Market Strength\n"
        "Rather Than Physical Geography"
    ),
    fontsize=28,
    color="white",
    pad=35,
    fontweight="bold"
)

# --------------------------------------------------
# DECORATION
# --------------------------------------------------

ax.text(
    -52_000_000,
    52_000_000,
    "Projection: SK-Orbital v1.0",
    color="white",
    fontsize=10,
    alpha=0.7
)

ax.text(
    -52_000_000,
    49_000_000,
    "Day 25 • Is This A Map?",
    color="white",
    fontsize=10,
    alpha=0.7
)

ax.text(
    -52_000_000,
    46_000_000,
    "Source: Last.fm Listener Data",
    color="white",
    fontsize=10,
    alpha=0.7
)

# --------------------------------------------------
# NORTH ARROW
# --------------------------------------------------

ax.annotate(
    "",
    xy=(50_000_000, 45_000_000),
    xytext=(50_000_000, 35_000_000),
    arrowprops=dict(
        facecolor="white",
        width=4,
        headwidth=20
    )
)

ax.text(
    50_000_000,
    47_500_000,
    "GALACTIC\nNORTH",
    ha="center",
    color="white",
    fontsize=10
)

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

ax.set_aspect("equal")

ax.set_xlim(
    -65_000_000,
    65_000_000
)

ax.set_ylim(
    -65_000_000,
    65_000_000
)

ax.axis("off")

plt.tight_layout()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

plt.savefig(
    OUTPUT,
    dpi=400,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.show()

print(f"\nSaved to: {OUTPUT}")