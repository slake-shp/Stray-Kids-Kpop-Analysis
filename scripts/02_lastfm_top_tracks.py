from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

api_key = os.getenv("LASTFM_API_KEY")

url = (
    "https://ws.audioscrobbler.com/2.0/"
    "?method=artist.gettoptracks"
    "&artist=Stray+Kids"
    f"&api_key={api_key}"
    "&format=json"
    "&limit=50"
)

response = requests.get(url)

data = response.json()

records = []

for track in data["toptracks"]["track"]:

    records.append({
        "track": track["name"],
        "listeners": track["listeners"],
        "playcount": track["playcount"]
    })

tracks_df = pd.DataFrame(records)

tracks_df.to_csv(
    "data/raw/stray_kids_top_tracks.csv",
    index=False
)

print(tracks_df.head())