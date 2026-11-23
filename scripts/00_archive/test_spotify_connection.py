from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

print("Client ID starts:", client_id[:4])
print("Client Secret starts:", client_secret[:4])
print("Client ID length:", len(client_id))
print("Client Secret length:", len(client_secret))