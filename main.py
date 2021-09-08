from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

pp = pprint.PrettyPrinter(indent=1)

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"

spotify_username = "31o53o6rfgnxmk7stxmzun6h7sru"
client_id = "744d0830ec4049ca9486e00e8b621a97"
client_secret = "569ba1b015db4171b79a718db9fa63bf"
redirect_uri = "http://example.com"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path=".cache"
    )
)

user_id = sp.current_user()["id"]
date = input("Which year you would like to travel to? Type the date in this format YYYY-MM-DD:  ")
response = requests.get(f"{BILLBOARD_URL}/{date}")
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
musics = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [music.getText() for music in musics]


# 1995-02-19
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    collaborative=False,
    description=""
)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

