import os
import requests

# Can we curl the lobby and get a random user???
# http://crawl.akrasiac.org:8080/#lobby
# TODO: find a random user from the lobby, if you don't supply one


def find_morgue_file(
    character=None, local_mode=False, morgue_file_path=None, morgue_url=None
):

    # find_morgue_filepath
    if morgue_file_path or local_mode:
        if morgue_file_path is None:
            if character is None:
                # TODO: Make this configurable
                character = "GucciMane"

            # TODO: Look up Platform defaults
            default_morgue_folder = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue"
            morgue_folder = os.environ.get("MORGUE_FOLDER", default_morgue_folder)
            morgue_file_path = f"{morgue_folder}/{character}.txt"

        with open(morgue_file_path) as morgue_file:
            return morgue_file.read()
    else:

        # find_url
        if character:
            morgue_url = (
                f"http://crawl.akrasiac.org/rawdata/{character}/{character}.txt"
            )
        else:
            # TODO: Make this configurable, and unify the names
            username = "beginbot"
            morgue_url = f"http://crawl.akrasiac.org/rawdata/{username}/{username}.txt"
        return fetch_online_morgue(morgue_url)


def fetch_online_morgue(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"\033[031;1mCould not find the Character at {url}\033[0m")
        sys.exit()
