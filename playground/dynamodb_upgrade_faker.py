import boto3

# We need to pull this in some how
# We need Pulumi to dump and .env file!
TABLE_NAME = "characters-696d3eb"

character_name = "beginbot"

# objects = [ "the cursed +14 obsidian axe {chop, +Fly SInv *Curse}" ]
objects = [ "dumb weapon" ]

objects = ["very cool", "fake rune", "another2", "what", "hello", "slimey", "barnacled", "gold"]
# objects = ["barnacled", "slimy"]

client = boto3.client("dynamodb")

response = client.update_item(
    TableName=TABLE_NAME,
    Key={"character": {"S": character_name}},
    AttributeUpdates={
        # "weapons": {"Value": {f"SS": objects}, "Action": "PUT"}
        "runes": {"Value": {f"SS": objects}, "Action": "PUT"}
    },
)
print(response)
