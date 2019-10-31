import os
import boto3

from lib.character import Character
from lib.morgue_parser import fetch_xl_level
from lib.morgue_parser import fetch_weapons
from lib.morgue_parser import fetch_altars
from lib.morgue_parser import fetch_armour

from lib.the_real_morgue_parser import MorgueParser


TABLE_NAME = os.environ.get("CHARACTER_DB", "characters-696d3eb")


def fetch_and_save_weapons(character_name, morguefile):
    weapons = fetch_weapons(morguefile)
    morgue_db = MorgueDB(character_name)
    # morgue_db.delete_stuff("SS", "weapons")
    # morgue_db._create_character()
    # morgue_db.save_stuff("SS", "weapons", weapons)


def save_a_buncha_info(character_name):
    character = Character(name=character_name)
    morgue_db = MorgueDB(character_name)
    morgue_file = character.s3_morgue_file()
    morgue_parser = MorgueParser(morgue_file)
    try:
        runes = morgue_parser.runes()
        if runes:
            nice_runes = [rune.strip() for rune in runes.split(",")]
            morgue_db.save_stuff("SS", "runes", nice_runes)

        xl_level = fetch_xl_level(morgue_file)
        if xl_level:
            morgue_db.save_stuff("S", "xl", xl_level.strip())

        weapons = fetch_weapons(morgue_file)
        if weapons:
            morgue_db.save_stuff("SS", "weapons", weapons)

        # gods = fetch_altars(morgue_file)
        # morgue_db.save_stuff("SS", "gods", gods)

        armour = fetch_armour(morgue_file)
        if armour:
            morgue_db.save_stuff("SS", "armour", armour)
    except Exception as e:
        print(f"Error in save_a_buncha_info by we are ok: {e}")


class MorgueDB:
    def __init__(self, character_name):
        self.character_name = character_name
        self.client = boto3.client("dynamodb")

    # ========================================================================================

    def delete_stuff(self, db_type, name):
        response = self.client.delete_item(
            TableName=TABLE_NAME, Key={"character": {"S": self.character_name}}
        )
        print(f"\033[35m{response}\033[0m")

    def save_stuff(self, db_type, name, objects):
        # if objects:
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": self.character_name}},
            AttributeUpdates={
                name: {"Value": {f"{db_type}": objects}, "Action": "PUT"}
            },
        )
        print(f"\033[35m{response}\033[0m")
        # else:
        #     print(f"NOTHING TO SAVE: {name}")

    def save_armour(self, character_name, armour):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": character_name}},
            AttributeUpdates={"armour": {"Value": {"SS": armour}, "Action": "PUT"}},
        )

    def save_weapons(self, character_name, weapons):
        # "L": [ {"S": "Cookies"}

        try:
            response = self.client.update_item(
                TableName=TABLE_NAME,
                Key={"character": {"S": character_name}},
                # AttributeUpdates={"weapons": {"Value": {"SS": weapons}, "Action": "PUT"}},
                AttributeUpdates={
                    "weapons": {
                        "Value": {"L": [({"S": weapon}) for weapon in weapons]},
                        "Action": "PUT",
                    }
                },
            )
        except:
            print("TROUBLE IN PARADISE")
            print(weapons)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def save_xl(self, character_name, xl_level):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": character_name}},
            AttributeUpdates={"xl_level": {"Value": {"S": xl_level}, "Action": "PUT"}},
        )

    # ========================================================================================

    def _create_character(self):
        response = self.client.put_item(
            TableName=TABLE_NAME, Item={"character": {"S": self.character_name}}
        )
        print(response)

    def _fetch_seed(self):
        response = self.client.get_item(
            TableName=TABLE_NAME, Key={"character": {"S": self.character_name}}
        )
        if "seed" in response["Item"]:
            return response["Item"]["seed"]["S"]

    def _store_skills(self, skills):
        response = self.client.put_item(
            TableName=TABLE_NAME,
            Item={
                "character": {"S": self.character_name},
                "skills": {"SS": list(skills)},
            },
        )

    def _store_seed(self, seed):
        response = self.client.put_item(
            TableName=TABLE_NAME,
            Item={"character": {"S": self.character_name}, "seed": {"S": seed}},
        )

    # def _fetch_gods(self):
    #     response = self.client.get_item(
    #         TableName=TABLE_NAME, Key={"character": {"S": self.character_name}}
    #     )

    #     if "Item" in response:
    #         if "gods" in response["Item"]:
    #             return response["Item"]["gods"]["SS"]
    #         else:
    #             return []
    #     else:
    #         return []
