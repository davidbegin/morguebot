from lib.sns import send_unrand_notification
from lib.sns import send_morguefile_notification
from lib.character import Character
from lib.pawn_star import PawnStar


def process_dynamodb_records(event):
    for record in event["Records"]:
        gossiper = DungeonGossiper(record)
        new_unrands = gossiper.new_unrands()
        if new_unrands:
            print(f"PRINT WE FOUND NEW UNRAND {new_unrands}")
            for unrand in new_unrands:
                send_unrand_notification(gossiper.character, unrand)
        else:
            print("PRINT WE FOUND NO NEW UNRAND")


class DungeonGossiper:
    def __init__(self, record):
        self.record = record
        dynamodb_record = self.record["dynamodb"]
        name = dynamodb_record["Keys"]["character"]["S"]
        self.character = Character(name=name)

        dynamodb_record = self.record["dynamodb"]

        new_image = dynamodb_record["NewImage"]
        if "weapons" in new_image:
            self.current_weapons = new_image["weapons"]["SS"]
        else:
            self.current_weapons = []

        if "OldImage" in dynamodb_record:
            old_image = dynamodb_record["OldImage"]
            if "weapons" in old_image:
                self.old_weapons = old_image["weapons"]["SS"]
            else:
                self.old_weapons = []
        else:
            self.old_weapons = []

    def new_weapons(self):
        return list(set(self.current_weapons) - set(self.old_weapons))

    def new_unrands(self):
        # unrands = [ weapon for weapon in self.current_weapons if PawnStar(weapon).is_unrand() ]
        unrands = [
            weapon for weapon in self.new_weapons() if PawnStar(weapon).is_unrand()
        ]
        if unrands:
            return unrands
        else:
            return []
