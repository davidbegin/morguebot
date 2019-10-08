import os
import requests

# Can we curl the lobby and get a random user???
# http://crawl.akrasiac.org:8080/#lobby
# TODO: find a random user from the lobby, if you don't supply one

# Print the Location


def find_morgue_filepath(character=None):
    if character is None:
        # TODO: Make this configurable
        character = "GucciMane"

    # TODO: Look up Platform defaults
    default_morgue_folder = (
        f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue"
    )
    morgue_folder = os.environ.get("MORGUE_FOLDER", default_morgue_folder)
    return f"{morgue_folder}/{character}.txt"


def find_morgue_url(character=None, morgue_url=None):
    if character:
        morgue_url = f"http://crawl.akrasiac.org/rawdata/{character}/{character}.txt"
    else:
        # TODO: Make this configurable, and unify the names
        username = "beginbot"
        morgue_url = f"http://crawl.akrasiac.org/rawdata/{username}/{username}.txt"

    return morgue_url


def fetch_morgue_file(
    local_mode=False, character=None, morgue_filepath=None, morgue_url=None
):
    if local_mode:
        if morgue_filepath is None:
            morgue_filepath = find_morgue_filepath(character=character)
        return open(morgue_filepath).read()
    else:
        if morgue_url is None:
            morgue_url = find_morgue_url(character)
        return _fetch_online_morgue(morgue_url)


# TODO: add suggestions for fun!
def _fetch_online_morgue(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"\033[031;1mCould not find the Character at {url}\033[0m")
        sys.exit()
