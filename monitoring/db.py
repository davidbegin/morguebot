import boto3
import time

# We want to keep looking at this DynamoDB table
# and printing the items

client = boto3.client("dynamodb")
TABLE_NAME = "characters-696d3eb"


# {'xl_xl': {'S': '6'}, 'character': {'S': 'Jeffwins'}, 'weapons': {'SS': [' a - a +0 short sword (weapon)', ' g - 49 stones (quivered)', ' h - 33 arrows', ' i - 26 bolts', ' p - 4 boomerangs', 'Armour', 'Missiles']}, 'xl': {'S': '1'}, 'armour': {'SS': [' t - a cursed +0 buckler (worn)', 'Jewellery']}}

def monitor_runes():
    response = client.scan(
            TableName=TABLE_NAME,
            Select="ALL_ATTRIBUTES",
            )

    all_runes = []
    for item in response["Items"]:
        character_name = item["character"]["S"]
        if "runes" in item:
            runes = item["runes"]["SS"]
        else:
            runes = []

        all_runes.append({"name": character_name, "runes": runes})
    sorted_runes = sorted(all_runes, key=lambda k: len(k['runes']))
    sorted_runes.reverse()
    winners = sorted_runes[0:5]

def monitor_characters():
    while True:
        response = client.scan(
            TableName=TABLE_NAME
        )
        characters_in_db = [ character['character']['S'] for character in response['Items'] ]
        print(characters_in_db)
        time.sleep(5)

def monitor_character(character):
    while True:
        response = client.get_item(
            TableName=TABLE_NAME, Key={"character": {"S": character}}
        )

        if "Item" in response:
            item = response["Item"]
            for key in item.keys():
                print(f"{item[key]}\n")
        time.sleep(2)


# monitor_character("None")
# monitor_character("artmatt")
# monitor_characters()
monitor_runes()
