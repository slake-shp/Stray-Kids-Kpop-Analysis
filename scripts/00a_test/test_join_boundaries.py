import pandas as pd
import geopandas as gpd

# Load boundaries
world = gpd.read_file(
    "data/boundaries/natural_earth/ne_50m_admin_0_countries.shp"
)

# Load Stray Kids data
stats = pd.read_csv(
    "data/processed/stray_kids_country_stats.csv"
)

# Join
joined = world.merge(
    stats,
    left_on="ADM0_A3",
    right_on="iso3",
    how="left"
)

# Check matched countries
matches = joined[
    joined["stray_kids_market_strength"].notna()
]

print(
    f"Matched countries: {len(matches)}"
)

print(
    matches[
        [
            "NAME",
            "ISO_A3",
            "stray_kids_market_strength"
        ]
    ]
)
