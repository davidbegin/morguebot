import os
import json

from lib.character import Character
from lib.kinesis import send_chat_to_stream
from lib.pawn_star import PawnStar


def checkout_the_weapons(event):
    for record in event["Records"]:
        body = record["body"]
        _look_for_unrands(body)


# This is OLD Begin's of private
# This a convention
def _look_for_unrands(msg):
    try:
        new_unrands = []
        # Why are we decoded as the first thing we do in a function???
        decoded_msg = json.loads(msg)
        message = decoded_msg["Message"]

        print(f"\033[33mmessage: {message}\033[0m")

        character_weapon_info = json.loads(message)
        character = Character(name=character_weapon_info["character"])

        new_weapons = character_weapon_info["weapons"]

        new_unrands = [weapon for weapon in new_weapons if PawnStar(weapon).is_unrand()]

        if new_unrands:
            send_chat_to_stream(
                f"OSFrog {character.name} got a New Unrand! OSFrog {' || '.join(new_unrands)}"
            )
    except Exception as e:
        print(f"Error: {e} | msg: {msg}")
