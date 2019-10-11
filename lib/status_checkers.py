import boto3

from lib.morgue_parser import fetch_altars


def validate_seed(character):
    pass
    # old_seed = _fetch_seed(character.character)

    # if old_seed != character.seed:
    #     print("New Seeds!")
    #     _store_seed(character.character, character.seed)


# Fun Fact: There are currently 25 gods in DC
def check_for_new_gods(character, printer):
    old_altars = _fetch_gods(character.character)
    altars = set(fetch_altars(character.morgue_file()))

    print(f"old_altars: {old_altars}")
    print(f"altars: {altars}")

    if len(altars) > len(old_altars):
        new_altars = altars.difference(set(old_altars))
        print(f"We Found a new God(s): {new_altars}")
        printer.print_missionary(new_altars)

    if len(altars) > 0:
        _store_gods(character.character, list(altars))


TABLE_NAME = "morguebot"

client = boto3.client("dynamodb")


def _fetch_seed(character):
    response = client.get_item(
        TableName=TABLE_NAME, Key={"character": {"S": character}}
    )
    if "seed" in response["Item"]:
        return response["Item"]["seed"]["S"]


def _store_seed(character, seed):
    response = client.put_item(
        TableName=TABLE_NAME, Item={"character": {"S": character}, "seed": {"S": seed}}
    )


def _fetch_gods(character):
    response = client.get_item(
        TableName=TABLE_NAME, Key={"character": {"S": character}}
    )

    if "Item" in response:
        if "gods" in response["Item"]:
            return response["Item"]["gods"]["SS"]
        else:
            return []
    else:
        return []


# SO this update way is the wave
# We need this for all updates
def _store_gods(character, gods):
    response = client.update_item(
        TableName=TABLE_NAME,
        Key={"character": {"S": character}},
        AttributeUpdates={"gods": {"Value": {"SS": gods}, "Action": "PUT"}},
    )
