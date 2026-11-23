from dotenv import load_dotenv
import os
import requests
import pandas as pd
from pathlib import Path

# ----------------------------------
# Load API Key
# ----------------------------------

load_dotenv()

api_key = os.getenv("LASTFM_API_KEY")

if not api_key:
    raise ValueError("LASTFM_API_KEY not found")

# ----------------------------------
# Request Artist Info
# ----------------------------------

url = (
    "https://ws.audioscrobbler.com/2.0/"
    "?method=artist.getinfo"
    "&artist=Stray+Kids"
    f"&api_key={api_key}"
    "&format=json"
)

response = requests.get(url)

data = response.json()

artist = data["artist"]

# ----------------------------------
# Extract Information
# ----------------------------------

artist_data = pd.DataFrame([
    {
        "artist": artist["name"],
        "listeners": artist["stats"]["listeners"],
        "playcount": artist["stats"]["playcount"],
        "lastfm_url": artist["url"]
    }
])

# ----------------------------------
# Output Folder
# ----------------------------------

Path("data/raw").mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------
# Save CSV
# ----------------------------------

artist_data.to_csv(
    "data/raw/stray_kids_artist_info.csv",
    index=False
)

print(artist_data)
print("\nSaved: data/raw/stray_kids_artist_info.csv")