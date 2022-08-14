import re

import requests
from bs4 import BeautifulSoup


def get_attendees_from_setlist(url: str) -> list[str]:
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    attend = soup.find(class_="attendBox")
    profiles = attend.next_sibling.next_sibling
    users = profiles.find_all(title=re.compile("^View profile of"))
    usernames = [u.span.text for u in users]
    return usernames
