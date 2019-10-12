import boto3

TABLE_NAME = "morguebot"


class MorgueDB:
    def __init__(self, character):
        self.character = character
        self.character_name = character.character
        self.client = boto3.client("dynamodb")

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

    def _fetch_gods(self):
        response = self.client.get_item(
            TableName=TABLE_NAME, Key={"character": {"S": self.character_name}}
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
    def _store_gods(self, gods):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": self.character_name}},
            AttributeUpdates={"gods": {"Value": {"SS": gods}, "Action": "PUT"}},
        )
