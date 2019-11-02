import boto3


TABLE_NAME = "morguebot"

client = boto3.client("dynamodb")

def fetch_gods(character):
    response = client.get_item(TableName=TABLE_NAME, Key={"character": {"S": "beginbot"}})
    return response['Item']['gods']['SS']
    # Parse the Gods out



def store_gods(character, gods):
    response = client.put_item(
        TableName=TABLE_NAME,
        Item={
            "character": {"S": character},
            "gods": {"SS": gods}
        },
    )


store_gods("beginbot", ["Xin", "Zom", "Zorg"])
print(x)
x = fetch_gods("beginbot")
print(x)
