from dotenv import load_dotenv
import os
import requests
import pandas as pd
from pathlib import Path

# ==================================================
# Load API Key
# ==================================================

load_dotenv()

api_key = os.getenv("LASTFM_API_KEY")

if not api_key:
    raise ValueError("LASTFM_API_KEY not found")

# ==================================================
# Countries - added in iso3 values 
# ==================================================

countries = {
    "Korea, Republic of": {
        "display": "South Korea",
        "iso3": "KOR"
    },
    "Japan": {
        "display": "Japan",
        "iso3": "JPN"
    },
    "Philippines": {
        "display": "Philippines",
        "iso3": "PHL"
    },
    "Thailand": {
        "display": "Thailand",
        "iso3": "THA"
    },
    "Indonesia": {
        "display": "Indonesia",
        "iso3": "IDN"
    },
    "Australia": {
        "display": "Australia",
        "iso3": "AUS"
    },
    "United Kingdom": {
        "display": "United Kingdom",
        "iso3": "GBR"
    },
    "Germany": {
        "display": "Germany",
        "iso3": "DEU"
    },
    "France": {
        "display": "France",
        "iso3": "FRA"
    },
    "United States": {
        "display": "United States",
        "iso3": "USA"
    },
    "Canada": {
        "display": "Canada",
        "iso3": "CAN"
    },
    "Brazil": {
        "display": "Brazil",
        "iso3": "BRA"
    },
    "Mexico": {
        "display": "Mexico",
        "iso3": "MEX"
    }
}

# ==================================================
# Last.fm Country Ranking
# ==================================================

def get_artist_rank(country_name):

    url = (
        "https://ws.audioscrobbler.com/2.0/"
        "?method=geo.gettopartists"
        f"&country={country_name}"
        f"&api_key={api_key}"
        "&format=json"
        "&limit=1000"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "topartists" not in data:
        return None

    artists = data["topartists"]["artist"]

    for artist in artists:

        if artist["name"].strip().lower() == "stray kids":

            return {
                "rank": artist.get("@attr", {}).get("rank"),
                "listeners": artist.get("listeners")
            }

    return {
        "rank": 1000,
        "listeners": 0
    }

# ==================================================
# World Bank Population from 03a_get_population_data.py
# ==================================================

def get_population(iso3):

    url = (
        f"https://api.worldbank.org/v2/country/{iso3}"
        "/indicator/SP.POP.TOTL"
        "?format=json"
        "&mrv=1"
    )

    response = requests.get(url)

    try:
        return response.json()[1][0]["value"]
    except Exception:
        return None

# ==================================================
# Build Dataset
# ==================================================

records = []

for api_country, info in countries.items():

    print(f"Checking {info['display']}")

    result = get_artist_rank(api_country)

    population = get_population(
        info["iso3"]
    )

    if result is None:
        continue

    records.append({
        "country": info["display"],
        "iso3": info["iso3"],
        "rank": result["rank"],
        "listeners": result["listeners"],
        "population": population
    })

# ==================================================
# DataFrame
# ==================================================

df = pd.DataFrame(records)

df["rank"] = pd.to_numeric(
    df["rank"],
    errors="coerce"
)

df["listeners"] = pd.to_numeric(
    df["listeners"],
    errors="coerce"
)

df["population"] = pd.to_numeric(
    df["population"],
    errors="coerce"
)

# ==================================================
# Create Metrics
# ==================================================

df["inverse_rank"] = (
    1001 - df["rank"]
)

df["stray_kids_market_strength"] = (
    df["inverse_rank"]
    / df["population"]
    * 1000000
)

# ==================================================
# Rankings
# ==================================================

df = df.sort_values(
    "rank"
)

# ==================================================
# Save
# ==================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

output_file = (
    "data/processed/"
    "stray_kids_country_stats.csv"
)

df.to_csv(
    output_file,
    index=False
)

# ==================================================
# Validation Checks
# ==================================================

print("\nValidation Checks")

print(
    f"Countries analysed: {len(df)}"
)

print(
    f"Missing populations: "
    f"{df['population'].isna().sum()}"
)

print(
    f"Missing ranks: "
    f"{df['rank'].isna().sum()}"
)

print(
    f"Missing listeners: "
    f"{df['listeners'].isna().sum()}"
)

print(
    f"Missing market strength values: "
    f"{df['stray_kids_market_strength'].isna().sum()}"
)

duplicates = (
    df["country"]
    .duplicated()
    .sum()
)

print(
    f"Duplicate countries: "
    f"{duplicates}"
)

assert len(df) > 0, (
    "No country records returned."
)

assert (
    df["population"]
    .notna()
    .all()
), (
    "Population data missing."
)

assert (
    df["rank"]
    .notna()
    .all()
), (
    "Rank data missing."
)

assert (
    df["stray_kids_market_strength"]
    .notna()
    .all()
), (
    "Market strength contains NULL values."
)

assert (
    df["population"] > 0
).all(), (
    "Population contains zero or negative values."
)

assert (
    df["rank"] > 0
).all(), (
    "Rank contains invalid values."
)

assert duplicates == 0, (
    f"{duplicates} duplicate countries found."
)

print("✓ All validation checks passed")

# ==================================================
# Summary
# ==================================================

print("\nTop Countries")

print(
    df[
        [
            "country",
            "rank",
            "population",
            "stray_kids_market_strength"
        ]
    ]
)

print(
    f"\nSaved: {output_file}"
)