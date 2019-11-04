COMMANDS = {
    "meta": ["!h?"],
    "single_character": [
        "!armour",
        "!fetch",
        "!fetch_s3_morgue",
        "!jewellery",
        "!max_damage",
        "!mutations",
        "!overview",
        "!potions",
        "!runes",
        "!save_morgue",
        "!scrolls",
        "!search",
        "!skills",
        "!spells",
        "!version",
        "!weapons",
    ],
    "all_characters": [
        "!characters",
        "!clean_morgue",
        "!fetch_runes",
        "!rune_awards",
        "!stalk_all",
        "!weapon_awards",
    ],
}


class MorgueBotCommand:
    pass


# We need to check if the command is valid
# if its a single character, if it has a character
# if it takes extra args, what are those extra args
class MorgueEvent:
    def __init__(
        self, command, character=None, search=None, level_barrier=None, args=[]
    ):
        self.command = command
        self.character = character
        self.search = search
        self.level_barrier = level_barrier
        self.args = args

    @classmethod
    def from_event(cls, event):
        command = event["command"]
        character = event["character"]

        if "level_barrier" in event:
            level_barrier = event["level_barrier"]
        else:
            level_barrier = None

        if "args" in event:
            args = event["args"]
        else:
            args = []

        if "search" in event:
            search = event["search"]
        else:
            search = None

        return cls(
            command=command,
            character=character,
            level_barrier=level_barrier,
            search=search,
            args=args,
        )

    def is_character_command(self):
        return self.command in COMMANDS["single_character"]
