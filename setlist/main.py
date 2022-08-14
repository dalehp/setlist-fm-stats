from collections import Counter

from setlist.api import get_mbid_for_artist, get_setlists_including_song
from setlist.scrape import get_attendees_from_setlist


def main():
    artist = "black midi"
    mbid = get_mbid_for_artist(artist)
    setlist_urls = get_setlists_including_song(mbid, "Dangerous Liasons")

    user_song_counts = Counter()
    for s_url in setlist_urls:
        attendees = get_attendees_from_setlist(s_url)
        user_song_counts += Counter(attendees)
    print(user_song_counts)
