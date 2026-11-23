import geopandas as gpd

gdf = gpd.read_file(
    "data/boundaries/natural_earth/ne_50m_admin_0_countries.shp"
)

print(f"Countries: {len(gdf)}")

print("\nColumns:")
print(gdf.columns.tolist())