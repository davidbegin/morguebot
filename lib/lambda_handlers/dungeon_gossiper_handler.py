from lib.dungeon_gossiper import DungeonGossiper
from lib.command_executor import process_event
from lib.kinesis import send_new_runes_msg
from lib.sns import send_new_weapons_notification


class DungeonGossiperHandler:
    def __init__(self, event):
        self.event = event

    def handle():
        print("I am proud to serve you as your new DungeonGossiper(Handler)")
        if "Records" in self.event:
            for record in self.event["Records"]:
                gossiper = DungeonGossiper(record)
                # check_for_unrands(gossiper)
                if gossiper.new_weapons():
                    print(f"We got some new weapons: {gossiper.new_weapons()}")
                    send_new_weapons_notification(
                        gossiper.character, gossiper.new_weapons()
                    )
                if gossiper.new_runes():
                    print(f"We Got new runes {gossiper.new_runes()}")
                    send_new_runes_msg(gossiper.character, gossiper.new_runes())
        else:
            process_event(self.event)
