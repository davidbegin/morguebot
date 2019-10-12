TABLE_NAME = "morguebot"


class MorgueDB:
   def __init__(self, character=character):
        self.character = character
        self.client = boto3.client("dynamodb")

    def _fetch_seed():
        response = self.client.get_item(
            TableName=TABLE_NAME, Key={"character": {"S": self.character}}
        )
        if "seed" in response["Item"]:
            return response["Item"]["seed"]["S"]

    def _store_skills(skills):
        response = self.client.put_item(
            TableName=TABLE_NAME,
            Item={"character": {"S": self.character}, "skills": {"SS": list(skills)}},
        )

    def _store_seed(seed):
        response = self.client.put_item(
            TableName=TABLE_NAME,
            Item={"character": {"S": self.character}, "seed": {"S": seed}},
        )

    def _fetch_gods():
        response = self.client.get_item(
            TableName=TABLE_NAME, Key={"character": {"S": self.character}}
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
    def _store_gods(gods):
        response = self.client.update_item(
            TableName=TABLE_NAME,
            Key={"character": {"S": self.character}},
            AttributeUpdates={"gods": {"Value": {"SS": gods}, "Action": "PUT"}},
        )
