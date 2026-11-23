import requests
import pandas as pd
from pathlib import Path

countries = {
    "South Korea": "KOR",
    "Japan": "JPN",
    "Philippines": "PHL",
    "Thailand": "THA",
    "Indonesia": "IDN",
    "Australia": "AUS",
    "United Kingdom": "GBR",
    "Germany": "DEU",
    "France": "FRA",
    "United States": "USA",
    "Canada": "CAN",
    "Brazil": "BRA",
    "Mexico": "MEX"
}

records = []

for country, iso3 in countries.items():

    url = (
        f"https://api.worldbank.org/v2/country/{iso3}"
        "/indicator/SP.POP.TOTL"
        "?format=json"
        "&mrv=1"
    )

    response = requests.get(url)

    data = response.json()

    population = data[1][0]["value"]

    records.append({
        "country": country,
        "iso3": iso3,
        "population": population
    })

population_df = pd.DataFrame(records)

Path("data/raw").mkdir(
    parents=True,
    exist_ok=True
)

population_df.to_csv(
    "data/raw/world_bank_population.csv",
    index=False
)

print(population_df)