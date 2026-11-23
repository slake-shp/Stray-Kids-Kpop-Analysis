from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("LASTFM_API_KEY")

countries = [
    "South Korea",
    "Korea",
    "Korea, Republic of",
    "Republic of Korea"
]

for country in countries:

    url = (
        "https://ws.audioscrobbler.com/2.0/"
        "?method=geo.gettopartists"
        f"&country={country}"
        f"&api_key={api_key}"
        "&format=json"
        "&limit=1"
    )

    response = requests.get(url)

    data = response.json()

    if "topartists" in data:
        print(f"✓ Works: {country}")
    else:
        print(f"✗ Fails: {country}")
        print(data)