import os
import json

import boto3

from lib.character import Character
from lib.pawn_star import PawnStar


# def check_for_unrands(gossiper):
#     new_unrands = [
#         weapon for weapon in gossiper.new_weapons() if PawnStar(weapon).is_unrand()
#     ]
#     if new_unrands:
#         print(f"PRINT WE FOUND NEW UNRAND {new_unrands}")
#         for unrand in new_unrands:
#             send_unrand_notification(gossiper.character, unrand)
#     else:
#         print(f"\033[33mSorry {gossiper.character} no new unrand\033[0m")


def checkout_the_weapons(event):
    print(json.dumps(event))

    for record in event["Records"]:
        body = record["body"]
        _send_chat(body)


def _send_chat(msg):
    # IF debug mode:
    # print(f"Weapons Bot Time! {msg}")
    kinesis_arn = os.environ["CHAT_STREAM_ARN"]
    kinesis_name = os.environ["CHAT_STREAM_NAME"]

    client = boto3.client("kinesis")

    # OSFrog New Weapons
    try:
        new_unrands = []
        decoded_msg = json.loads(msg)
        message = decoded_msg["Message"]
        print(f"message: {message}")
        character_weapon_info = json.loads(decoded_msg["Message"])
        character = Character(name=character_weapon_info["character"])
        new_weapons = character_weapon_info["weapons"]
        new_unrands = [weapon for weapon in new_weapons if PawnStar(weapon).is_unrand()]
        if new_unrands:
            response = client.put_record(
                StreamName=kinesis_name,
                Data=json.dumps(
                    {
                        "Message": f"OSFrog {character.name} got a New Unrand! OSFrog {' || '.join(new_unrands)}"
                    }
                ),
                PartitionKey="alpha",
            )
            print(response)
    except Exception as e:
        print(f"Error: {e} | msg: {msg}")
