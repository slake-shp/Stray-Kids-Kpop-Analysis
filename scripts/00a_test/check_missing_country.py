import pandas as pd
import geopandas as gpd

world = gpd.read_file(
    "data/boundaries/natural_earth/ne_50m_admin_0_countries.shp"
)

stats = pd.read_csv(
    "data/processed/stray_kids_country_stats.csv"
)

print("Countries in stats file:")
print(sorted(stats["iso3"].unique()))

print("\nCountries in join:")

joined = world.merge(
    stats,
    left_on="ISO_A3",
    right_on="iso3",
    how="left"
)

matched = set(
    joined.loc[
        joined["stray_kids_market_strength"].notna(),
        "ISO_A3"
    ]
)

print(sorted(matched))

print("\nMissing:")

missing = set(
    stats["iso3"]
) - matched

print(missing)