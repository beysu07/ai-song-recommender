from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random, os
from dotenv import load_dotenv

# ---------------- SETUP ----------------
app = Flask(__name__)
load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)

onceki_sarkilar = set()

# ---------------- PLAYLIST ARAMA HAVUZU ----------------
# ID YOK → SEARCH VAR → Spotify API patlamaz

PLAYLIST_QUERIES = {
    "turkish_2000s": [
        "2000'ler türkçe pop",
        "turkish pop classics",
        "turkish pop 2000s"
    ],
    "turkish_2010s": [
        "2010'lar türkçe pop",
        "turkish pop 2010s"
    ],
    "turkish_2020s": [
        "turkish pop hits",
        "turkey top hits"
    ],
    "global_2000s": [
        "all out 2000s",
        "2000s pop classics"
    ],
    "global_2010s": [
        "all out 2010s",
        "2010s pop hits"
    ],
    "global_2020s": [
        "today's top hits",
        "global pop hits"
    ]
}

# ---------------- CÜMLE ANALİZ ----------------

def cumle_analiz(niyet):
    t = niyet.lower()

    if any(k in t for k in ["final", "vize", "sınav", "imtihan", "ders"]):
        return "akademik_stres"
    if any(k in t for k in ["hava", "güzel", "bahar", "güneş"]):
        return "mutlu_an"
    if any(k in t for k in ["yoruldum", "bıktım", "tükendim"]):
        return "tukenmislik"
    if any(k in t for k in ["imdat", "yetişemiyorum", "üst üste"]):
        return "panik"
    if any(k in t for k in ["gaz", "motive", "başar"]):
        return "motivasyon"

    return "genel"

# ---------------- DÖNEM & DİL KARARI ----------------

def donem_ve_dil_sec(durum):
    if durum in ["akademik_stres", "motivasyon", "mutlu_an"]:
        return random.choice(["turkish_2010s", "turkish_2020s"])
    if durum in ["tukenmislik", "panik"]:
        return random.choice(["global_2000s", "global_2010s"])
    return random.choice(list(PLAYLIST_QUERIES.keys()))

# ---------------- ÇALIŞAN PLAYLIST BUL ----------------

def calisan_playlist_bul(query):
    try:
        results = sp.search(q=query, type="playlist", limit=5)
        for pl in results["playlists"]["items"]:
            try:
                sp.playlist_items(pl["id"], limit=1)
                return pl["id"]
            except:
                continue
    except:
        return None

    return None

# ---------------- SPOTIFY MOTORU ----------------

def spotify_sarki_cek(niyet):
    durum = cumle_analiz(niyet)
    key = donem_ve_dil_sec(durum)
    query = random.choice(PLAYLIST_QUERIES[key])

    playlist_id = calisan_playlist_bul(query)
    if not playlist_id:
        return "Spotify'dan uygun playlist bulunamadı."

    try:
        results = sp.playlist_items(playlist_id, limit=50)
    except:
        return "Spotify'dan şarkı çekilemedi."

    tracks = [
        f"{item['track']['artists'][0]['name']} - {item['track']['name']}"
        for item in results["items"]
        if item.get("track")
        and f"{item['track']['artists'][0]['name']} - {item['track']['name']}" not in onceki_sarkilar
    ]

    if not tracks:
        onceki_sarkilar.clear()
        tracks = [
            f"{item['track']['artists'][0]['name']} - {item['track']['name']}"
            for item in results["items"]
            if item.get("track")
        ]

    secilen = random.choice(tracks)
    onceki_sarkilar.add(secilen)

    return secilen

# ---------------- ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    sarki = None

    if request.method == "POST":
        niyet = request.form["niyet"]
        sarki = spotify_sarki_cek(niyet)

    return render_template("index.html", sarki=sarki)

# ---------------- MAIN ----------------

if __name__ == "__main__":
    app.run(debug=True)