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


def _find_user():
    process = subprocess.Popen("whoami", stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8").strip()


if "DEFAULT_MORGUE_FOLDER" in os.environ:
    DEFAULT_MORGUE_FOLDER = os.environ["DEFAULT_MORGUE_FOLDER"]
else:
    DEFAULT_MORGUE_FOLDER = f"/Users/{_find_user()}/Library/Application Support/Dungeon Crawl Stone Soup/morgue"

MORGUE_DOMAIN = "http://crawl.akrasiac.org/rawdata"

if "MORGUE_BUCKETNAME" in os.environ:
    BUCKET = os.environ["MORGUE_BUCKETNAME"]
else:
    BUCKET = "morgue-files-2944dfb"


class Character:
    def __init__(
        self, morgue_filepath=None, morgue_url=None, character=None, local_mode=None
    ):
        self.morgue_filepath = morgue_filepath
        self.morgue_url = morgue_url
        self.character = character
        self.local_mode = local_mode
        self._find_character_and_morguefile()

        self.key = f"{character}/morguefile.txt"
        self.wielded_weapon = fetch_weapon(self.morgue_file)
        self.weapons = fetch_weapons(self.morgue_file)

    # This returns the max damages for all weapons
    def calc_max_damages(self):
        if not self.weapons:
            return ["No Weapons Found!"]

        max_damages = self._find_max_damages()

        if max_damages:
            return max_damages

    def _find_max_damages(self):
        max_damages = []
        for weapon in self.weapons:
            weapon = WeaponFactory(self.character, weapon)
            max_damage = weapon.max_damage()
            max_damages.append(
                {
                    "weapon": weapon.name,
                    "max_damage": max_damage,
                    "type": weapon.weapon_type,
                    "character": self.character_name,
                }
            )

        def sort_by_max_damage(elem):
            return elem["max_damage"]

        max_damages.sort(key=sort_by_max_damage)

        return max_damages

    def non_saved_morgue_file(self):
        if self.local_mode:
            morgue = open(self.morgue_filepath).read()
        else:
            morgue = self._fetch_online_morgue()
        return morgue

    def __str__(self):
        return self.character

    def __repr__(self):
        return f"{super().__repr__()}: {self.character}"

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
    def _fetch_online_morgue(self):
        response = requests.get(self.morgue_url)
        if response.status_code == 200:
            return response.text
        else:
            print(
                f"\033[031;1mCould not find the Character at {self.morgue_url}\033[0m"
            )
            # sys.exit()

    def _test(self):
        client = boto3.client("s3")
        response = client.get_object(Bucket=BUCKET, Key=self.key)
        morgue1 = response["Body"].read()

        morgue2 = self._fetch_online_morgue()
        # import pdb; pdb.set_trace()
