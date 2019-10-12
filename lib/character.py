import os
import sys
import subprocess

import requests

from lib.morgue_parser import fetch_seed
from lib.morgue_parser import fetch_turns
from lib.morgue_saver import morgue_saver


def _find_user():
    process = subprocess.Popen("whoami", stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8").strip()


if "DEFAULT_MORGUE_FOLDER" in os.environ:
    DEFAULT_MORGUE_FOLDER = os.environ["DEFAULT_MORGUE_FOLDER"]
else:
    DEFAULT_MORGUE_FOLDER = (
        f"/Users/{_find_user()}/Library/Application Support/Dungeon Crawl Stone Soup/morgue"
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

    def morgue_file(self):
        if self.local_mode:
            morgue = open(self.morgue_filepath).read()
        else:
            morgue = self._fetch_online_morgue(self.morgue_url)
        self.seed = fetch_seed(morgue)
        self.turns = fetch_turns(morgue)

        morgue_saver(self, morgue)
        return morgue

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

    # TODO: add suggestions for fun!
    def _fetch_online_morgue(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"\033[031;1mCould not find the Character at {url}\033[0m")
            sys.exit()
