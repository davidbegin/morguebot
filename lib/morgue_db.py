import os
import boto3

from lib.character import Character
from lib.morgue_parser import fetch_xl_level
from lib.morgue_parser import fetch_weapons
from lib.morgue_parser import fetch_altars
from lib.morgue_parser import fetch_armour


TABLE_NAME = os.environ["CHARACTER_DB"]


def save_a_buncha_info(character_name):
    print(f"WE inside save_a_buncha_info: {character_name}")
    character = Character(character=character_name)
    morgue_db = MorgueDB(character)
    morgue_file = character.morgue_file()

    xl_level = fetch_xl_level(morgue_file)
    morgue_db.save_stuff("S", "xl_xl", xl_level.strip())

    weapons = fetch_weapons(morgue_file)
    morgue_db.save_stuff("SS", "weapons", weapons)

    # gods = fetch_altars(morgue_file)
    # morgue_db.save_stuff("SS", "gods", gods)

    armour = fetch_armour(morgue_file)
    morgue_db.save_stuff("SS", "armour", armour)


class MorgueDB:
    def __init__(self, character):
        self.character = character
        self.character_name = character.character
        self.client = boto3.client("dynamodb")

    # ========================================================================================

    def save_stuff(self, db_type, name, objects):
        if objects:
            response = self.client.update_item(
                TableName=TABLE_NAME,
                Key={"character": {"S": self.character_name}},
                AttributeUpdates={
                    name: {"Value": {f"{db_type}": objects}, "Action": "PUT"}
                },
            )
            print(response)
        else:
            print(f"NOTHING TO SAVE: {name}")

    def save_armour(self, character_name, armour):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": character_name}},
            AttributeUpdates={"armour": {"Value": {"SS": armour}, "Action": "PUT"}},
        )

    def save_weapons(self, character_name, weapons):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": character_name}},
            AttributeUpdates={"weapons": {"Value": {"SS": weapons}, "Action": "PUT"}},
        )

    def save_xl(self, character_name, xl_level):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": character_name}},
            AttributeUpdates={"xl_level": {"Value": {"S": xl_level}, "Action": "PUT"}},
        )

    # ========================================================================================

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
