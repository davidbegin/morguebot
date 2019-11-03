class MorgueEventRouter:
    def __init__(self, morgue_event):
        self.morgue_event = morgue_event

    def dest_lambda(self):
        if self.morgue_event.command == "!fetch":
            return "morgue_stalker"
        else:
            return "dungeon_gossiper"
