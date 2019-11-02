from lib.sns import send_morguefile_notification
from lib.character import Character
from lib.pawn_star import PawnStar

from lib.kinesis import send_new_runes_msg


# What does the Gossiper do?
#   - Parses and routes DynamoDB records into SNS Messages
class DungeonGossiper:
    def __init__(self, record):

        self.record = record
        dynamodb_record = self.record["dynamodb"]
        name = dynamodb_record["Keys"]["character"]["S"]
        self.character = Character(name=name)

        dynamodb_record = self.record["dynamodb"]
        self.old_runes = []

        if "NewImage" in dynamodb_record:
            new_image = dynamodb_record["NewImage"]
            if "weapons" in new_image:
                self.current_weapons = new_image["weapons"]["SS"]
            else:
                self.current_weapons = []

            if "runes" in new_image:
                self.current_runes = new_image["runes"]["SS"]
            else:
                self.current_runes = []
        else:
            old_image = dynamodb_record["OldImage"]
            if "weapons" in old_image:
                self.current_weapons = old_image["weapons"]["SS"]
            else:
                self.current_weapons = []

            if "runes" in old_image:
                self.current_runes = old_image["runes"]["SS"]
            else:
                self.current_runes = []

        if "OldImage" in dynamodb_record:
            old_image = dynamodb_record["OldImage"]

            if "weapons" in old_image:
                self.old_weapons = old_image["weapons"]["SS"]
            else:
                self.old_weapons = []

            if "runes" in old_image:
                self.old_runes = old_image["runes"]["SS"]
            else:
                self.old_runes = []
        else:
            self.old_weapons = []

    def new_runes(self):
        return list(set(self.current_runes) - set(self.old_runes))

    def new_weapons(self):
        return list(set(self.current_weapons) - set(self.old_weapons))
