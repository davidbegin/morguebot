import boto3


TABLE_NAME = "characters-696d3eb"

client = boto3.client("dynamodb")

def fetch_gods(character):
    # response = client.get_item(TableName=TABLE_NAME, Key={"character": {"S": "beginbot"}})
    response = client.get_item(TableName=TABLE_NAME, Key={"character": {"S": character}})
    i = response["Item"]
    print(i)
    import pdb; pdb.set_trace()
    return response
    # return response['Item']['gods']['SS']
    # return response['Item']['gods']['SS']
    # Parse the Gods out


def store_gods(character, gods):
    response = client.put_item(
        TableName=TABLE_NAME,
        Item={
            "character": {"S": character},
            "gods": {"SS": gods}
        },
    )


# store_gods("beginbot", ["Xin", "Zom", "Zorg"])
# print(x)
# import pdb; pdb.set_trace()
x = fetch_gods("kaostheory")
# print(x)
