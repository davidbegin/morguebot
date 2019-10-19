import boto3
import time

# We want to keep looking at this DynamoDB table
# and printing the items

client = boto3.client("dynamodb")
TABLE_NAME = "characters-696d3eb"


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
monitor_characters()
