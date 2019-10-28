from lib.sns import send_unrand_notification
from lib.character import Character

UNRANDS = [
    # "ring of the Mage {Wiz MR++ Int+3}",
    "the +12 Vampire's Tooth {vamp}",
    "+14 obsidian axe {chop, +Fly SInv *Curse}",
]


def process_dynamodb_records(event):
    for record in event["Records"]:
        gossiper = DungeonGossiper(record)
        new_unrands = gossiper.new_unrands()
        if new_unrands:
            for unrand in new_unrands:
                send_unrand_notification(gossiper.character, unrand)


class DungeonGossiper:
    def __init__(self, record):
        self.record = record
        dynamodb_record = self.record["dynamodb"]
        name = dynamodb_record["Keys"]["character"]["S"]
        self.character = Character(name=name)

    def new_weapons(self):
        dynamodb_record = self.record["dynamodb"]
        new_image = dynamodb_record["NewImage"]
        new_weapons = new_image["weapons"]["SS"]

        old_image = dynamodb_record["OldImage"]
        old_weapons = old_image["weapons"]["SS"]

        return list(set(new_weapons) - set(old_weapons))

    def new_unrands(self):
        new_unrands = [weapon for weapon in self.new_weapons() if weapon in UNRANDS]
        return new_unrands
