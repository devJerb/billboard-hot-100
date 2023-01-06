import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

BILLBOARD_HOT_100 = "https://www.billboard.com/charts/hot-100/"

# spotify client: https://developer.spotify.com/dashboard/applications/000779e62dec43ca9c50de9d8d0f8c36
CLIENT_ID = "client-id"
CLIENT_SECRET = "client-secret"
SPOTIFY_URI = "https://example.com/"
scope = "playlist-modify-private"

# get billboard hot 100 songs from given date
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
billboard_hot_100_webpage = requests.get(f"{BILLBOARD_HOT_100}{date}/").text

# scrape webpage for song titles
content = BeautifulSoup(billboard_hot_100_webpage, 'html.parser')
titles = [title.getText().strip() for title in content.select("ul li ul li h3", id="title-of-a-story")]
print(titles)

# authenticate spotify access
spotify_auth = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                         client_id=CLIENT_ID,
                                                         client_secret=CLIENT_SECRET,
                                                         redirect_uri=SPOTIFY_URI,
                                                         show_dialog=True,
                                                         cache_path="token.txt"
                                                         ))
user_id = spotify_auth.current_user()["id"]

# convert song titles to track ids
song_uri = []
year = date.split("-")[0]
for title in titles:
    search = spotify_auth.search(q=f'track: {title} year: {year}', type='track')
    try:
        result = search['tracks']['items'][0]['uri']
        song_uri.append(result)
    except IndexError:
        print(f"The song {title} does not exist.")

# create a playlist on Spotify
playlist = spotify_auth.user_playlist_create(user=user_id,
                                             name=f"Billboard Hot 100 of {year}",
                                             public=False,
                                             description=f"Top 100 hit songs of {year} made using Python."
                                             )
spotify_auth.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
print("Playlist created!")
