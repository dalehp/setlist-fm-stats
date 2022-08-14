from __future__ import annotations

from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

API_KEY = ""


class SetlistClient:
    BASE_URL = "https://api.setlist.fm/rest/1.0/"

    def __init__(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url: str, params: dict | None = None) -> dict:
        full_url = urljoin(self.BASE_URL, url)
        print(f"calling: {full_url}")
        resp = self.session.get(
            full_url,
            params=params or {},
            headers={"x-api-key": API_KEY, "Accept": "application/json"},
        )
        if resp.status_code == 429:
            breakpoint()
        resp.raise_for_status()
        return resp.json()


def get_mbid_for_artist(artist: str) -> str:
    # Hardcode to black midi mbid for now - need to disambiguate even for an exact match
    # so probably need to add a way for user to select based on description
    return "4afbef0a-05ee-4551-b0e0-f1f1870d8f1c"
    # c = SetlistClient()
    # resp = c.get(
    #     "search/artists", params={"artistName": "black midi", "sortOrder": "relevance"}
    # )


def song_in_setlist(song_name: str, setlist: dict) -> bool:
    for sets in setlist["sets"].values():
        for set_ in sets:
            for song in set_["song"]:
                if song_name == song["name"]:
                    return True
    return False


def get_setlists_including_song(mbid: str, song: str):
    c = SetlistClient()
    setlist_urls = []
    resp = c.get(f"artist/{mbid}/setlists")

    for setlist in resp["setlist"]:
        if song_in_setlist(song, setlist):
            setlist_urls.append(setlist["url"])

    pages = resp["total"] // resp["itemsPerPage"]
    print(f"{pages} API calls")
    for i in range(2, pages + 1):
        print(f"page {i}")
        resp = c.get(f"artist/{mbid}/setlists", params={"p": i})
        for setlist in resp["setlist"]:
            if song_in_setlist(song, setlist):
                setlist_urls.append(setlist["url"])
    return setlist_urls
