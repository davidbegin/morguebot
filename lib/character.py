import os
import sys
import requests

from lib.morgue_parser import fetch_seed

# Can we curl the lobby and get a random user???
# http://crawl.akrasiac.org:8080/#lobby
# TODO: find a random user from the lobby, if you don't supply one
# Print the Location
# TODO: Look up Platform defaults


DEFAULT_MORGUE_FOLDER = (
    f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue"
)
MORGUE_DOMAIN = "http://crawl.akrasiac.org/rawdata"


class Character:
    def __init__(
        self, morgue_filepath=None, morgue_url=None, character=None, local_mode=None
    ):
        self.morgue_filepath = morgue_filepath
        self.morgue_url = morgue_url
        self.character = character
        self.local_mode = local_mode

        self._find_character_and_morguefile()
        self._find_seed()

    def morgue_file(self):
        if self.local_mode:
            return open(self.morgue_filepath).read()
        else:
            return self._fetch_online_morgue(self.morgue_url)

    def _find_character_and_morguefile(self):
        if self.local_mode:
            if self.morgue_filepath is None:
                self.morgue_filepath = self._find_morgue_filepath()
        else:
            if self.character and self.morgue_url is None:
                self.morgue_url = self._find_morgue_url()
            if self.morgue_url is None:
                self.morgue_url = self._find_morgue_url()
        self._find_character()

    def _find_character(self):
        if self.character:
            pass

        if self.local_mode:
            morgue_path = self.morgue_filepath
        else:
            morgue_path = self.morgue_url
        self.character = morgue_path.split("/")[-1].replace(".txt", "")

    def _find_morgue_url(self):
        return f"{MORGUE_DOMAIN}/{self.character}/{self.character}.txt"

    def _find_morgue_filepath(self):
        morgue_folder = os.environ.get("MORGUE_FOLDER", DEFAULT_MORGUE_FOLDER)
        return f"{morgue_folder}/{self.character}.txt"

    def _find_seed(self):
        self.seed = fetch_seed(self.morgue_file())

    # TODO: add suggestions for fun!
    def _fetch_online_morgue(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"\033[031;1mCould not find the Character at {url}\033[0m")
            sys.exit()
