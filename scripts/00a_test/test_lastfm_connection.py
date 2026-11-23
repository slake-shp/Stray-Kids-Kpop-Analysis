from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("LASTFM_API_KEY")

print("API key found:", bool(api_key))

if api_key:
    print("API key length:", len(api_key))
    print("API key starts:", api_key[:4])

url = (
    "https://ws.audioscrobbler.com/2.0/"
    "?method=artist.getinfo"
    "&artist=Stray+Kids"
    f"&api_key={api_key}"
    "&format=json"
)

print("\nRequest URL:")
print(url)

response = requests.get(url)

print("\nStatus Code:", response.status_code)

print("\nResponse:")
print(response.text[:500])