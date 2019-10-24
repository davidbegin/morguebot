import os
import sys
import subprocess

import requests
import boto3

from lib.morgue_parser import fetch_seed
from lib.morgue_parser import fetch_turns
from lib.morgue_parser import fetch_weapon
from lib.morgue_parser import fetch_weapons
from lib.morgue_saver import morgue_saver

from lib.weapon_factory import WeaponFactory
from lib.morgue_folder_finder import find_morgue_folder


if "MORGUE_BUCKETNAME" in os.environ:
    BUCKET = os.environ["MORGUE_BUCKETNAME"]
else:
    BUCKET = "morgue-files-2944dfb"


class Character:
    def __init__(
        self, morgue_filepath=None, morgue_url=None, name=None, local_mode=None
    ):
        self.morgue_filepath = morgue_filepath
        self.morgue_url = morgue_url
        self.name = name

        # This upsets me past begin, what were you thinking?
        self.local_mode = local_mode
        self._find_name_and_morguefile()

        self.key = f"{name}/morguefile.txt"

        self.weapons = fetch_weapons(self.non_saved_morgue_file())

    # ========================================================================================

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{super().__repr__()}: {self.name}"

    # ========================================================================================

    def non_saved_morgue_file(self):
        if self.local_mode:
            morgue = open(self.morgue_filepath).read()
        else:
            morgue = self._fetch_online_morgue()
        return morgue

    def s3_morgue_file(self):
        try:
            client = boto3.client("s3")
            response = client.get_object(Bucket=BUCKET, Key=self.key)
            return response["Body"].read().decode()
        except Exception as e:
            print(f"Error fetching morguefile: {BUCKET} {self.key}")
            return None

    def morgue_file(self):
        if self.local_mode:
            morgue = open(self.morgue_filepath).read()
        elif BUCKET and self.key:
            morgue = self.s3_morgue_file()
            if morgue is None:
                morgue = self._fetch_online_morgue()
                morgue_saver(self, morgue)
        else:
            morgue = self._fetch_online_morgue()
        self.seed = fetch_seed(morgue)
        self.turns = fetch_turns(morgue)

        return morgue

    # We need a website morgue method

    # ========================================================================================

    def _find_name_and_morguefile(self):
        if self.local_mode:
            if self.morgue_filepath is None:
                self.morgue_filepath = self._find_morgue_filepath()
        else:
            self.morgue_url = self._find_morgue_url()
        self._find_name()

    def _find_name(self):
        if self.name:
            pass

        if self.local_mode:
            morgue_path = self.morgue_filepath
        else:
            morgue_path = self.morgue_url
        self.name = morgue_path.split("/")[-1].replace(".txt", "")

    def _find_morgue_url(self):
        MORGUE_DOMAIN = "http://crawl.akrasiac.org/rawdata"
        return f"{MORGUE_DOMAIN}/{self.name}/{self.name}.txt"

    def _find_morgue_filepath(self):
        return f"{find_morgue_folder()}/{self.name}.txt"

    def _fetch_online_morgue(self):
        response = requests.get(self.morgue_url)
        if response.status_code == 200:
            return response.text
        else:
            print(
                f"\033[031;1mCould not find the Character at {self.morgue_url}\033[0m"
            )
