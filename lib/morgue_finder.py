import os
import sys
import requests

# Can we curl the lobby and get a random user???
# http://crawl.akrasiac.org:8080/#lobby
# TODO: find a random user from the lobby, if you don't supply one

# Print the Location

# TODO: Look up Platform defaults
DEFAULT_MORGUE_FOLDER = (
    f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue"
)
MORGUE_DOMAIN = "http://crawl.akrasiac.org/rawdata"


def fetch_morgue_file(
    local_mode=False, character=None, morgue_filepath=None, morgue_url=None
):
    if local_mode:
        if morgue_filepath is None:
            morgue_filepath = _find_morgue_filepath(character=character)

        print(f"\033[37;1mUsing morgue_filepath: {morgue_filepath}\033[0m")
        return open(morgue_filepath).read()
    else:
        if morgue_url is None:
            morgue_url = _find_morgue_url(character)
        print(f"\033[037;1mUsing morgue_url: {morgue_url}\033[0m")
        return _fetch_online_morgue(morgue_url)


def _find_morgue_url(character="beginbot"):
    return f"{MORGUE_DOMAIN}/{character}/{character}.txt"


def _find_morgue_filepath(character="GucciMane"):
    morgue_folder = os.environ.get("MORGUE_FOLDER", DEFAULT_MORGUE_FOLDER)
    return f"{morgue_folder}/{character}.txt"


# TODO: add suggestions for fun!
def _fetch_online_morgue(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"\033[031;1mCould not find the Character at {url}\033[0m")
        sys.exit()
