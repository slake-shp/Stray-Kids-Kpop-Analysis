from pathlib import Path
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import os

# =====================================================
# Load Spotify Credentials
# =====================================================

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id:
    raise ValueError("SPOTIFY_CLIENT_ID not found in .env")

if not client_secret:
    raise ValueError("SPOTIFY_CLIENT_SECRET not found in .env")

# =====================================================
# Connect to Spotify
# =====================================================

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

print("Connected to Spotify")

# =====================================================
# Find Stray Kids
# =====================================================

results = sp.search(
    q="Stray Kids",
    type="artist",
    limit=1
)

artist = results["artists"]["items"][0]

artist_id = artist["id"]

print(f"Artist Found: {artist['name']}")
print(f"Spotify ID: {artist_id}")

# =====================================================
# Create Output Folder
# =====================================================

output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

# =====================================================
# Artist Metadata
# =====================================================

artist_metadata = pd.DataFrame([
    {
        "artist_name": artist["name"],
        "spotify_artist_id": artist["id"],
        "followers": artist["followers"]["total"],
        "spotify_popularity": artist["popularity"],
        "genres": ", ".join(artist["genres"]),
        "spotify_url": artist["external_urls"]["spotify"]
    }
])

artist_metadata.to_csv(
    output_folder / "artist_metadata.csv",
    index=False
)

print("Saved artist metadata")

# =====================================================
# Top Tracks
# =====================================================

top_tracks = sp.artist_top_tracks(artist_id)

track_records = []

for track in top_tracks["tracks"]:

    track_records.append(
        {
            "track_name": track["name"],
            "album": track["album"]["name"],
            "album_release_date": track["album"]["release_date"],
            "spotify_popularity": track["popularity"],
            "duration_minutes": round(
                track["duration_ms"] / 60000,
                2
            ),
            "track_url": track["external_urls"]["spotify"]
        }
    )

tracks_df = pd.DataFrame(track_records)

tracks_df.to_csv(
    output_folder / "spotify_stray_kids_top_tracks.csv",
    index=False
)

print("Saved top tracks")

# =====================================================
# Albums
# =====================================================

albums = sp.artist_albums(
    artist_id,
    album_type="album,single"
)

album_records = []

seen = set()

for album in albums["items"]:

    if album["name"] in seen:
        continue

    seen.add(album["name"])

    album_records.append(
        {
            "album_name": album["name"],
            "release_date": album["release_date"],
            "total_tracks": album["total_tracks"],
            "album_type": album["album_type"],
            "spotify_url": album["external_urls"]["spotify"]
        }
    )

albums_df = pd.DataFrame(album_records)

albums_df.sort_values(
    "release_date",
    inplace=True
)

albums_df.to_csv(
    output_folder / "spotify_stray_kids_albums.csv",
    index=False
)

print("Saved albums")

# =====================================================
# Summary
# =====================================================

print("\n=====================================")
print("STRAY KIDS DATA EXTRACTION COMPLETE")
print("=====================================")

print(
    f"Followers: "
    f"{artist['followers']['total']:,}"
)

print(
    f"Popularity: "
    f"{artist['popularity']}"
)

print(
    f"Top Tracks Retrieved: "
    f"{len(tracks_df)}"
)

print(
    f"Albums Retrieved: "
    f"{len(albums_df)}"
)

print("\nFiles Created:")

print(
    "data/raw/artist_metadata.csv"
)

print(
    "data/raw/spotify_stray_kids_top_tracks.csv"
)

print(
    "data/raw/spotify_stray_kids_albums.csv"
)