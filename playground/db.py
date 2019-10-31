import boto3

TABLE_NAME = "characters-696d3eb"

character_name = "beginbot"

# objects = [ "the cursed +14 obsidian axe {chop, +Fly SInv *Curse}" ]
# objects = [ "dumb weapon" ]

objects = ["very cool", "fake rune", "another2", "what"]
# objects = ["barnacled", "slimy"]

client = boto3.client("dynamodb")

response = client.update_item(
    TableName=TABLE_NAME,
    Key={"character": {"S": character_name}},
    AttributeUpdates={
        "runes": {"Value": {f"SS": objects}, "Action": "PUT"}
    },
)
print(response)
