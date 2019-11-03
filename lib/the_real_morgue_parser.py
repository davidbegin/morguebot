import re


class MorgueParser:
    def __init__(self, morgue_file):
        self.morgue_file = morgue_file

    def overview(self):
        user_stats = self.fetch_user_stats()
        xl_level = user_stats["xl"]
        health = user_stats["health"]

        location = self.fetch_location()

        m = re.search(f"(.*) Turns:\s(.*)", str(self.morgue_file))
        if m:
            return f"{m.group(1).strip()}  XL: {xl_level}  Health: {health}  Location: {location}".strip()

    def armour(self):
        pass

    # TODO: rename x and y
    def spells(self):
        x = "Your spell library contains the following spells:"
        y = "Dungeon Overview and Level Annotations"
        split_morgue_file = self.morgue_file.split("\n")
        start_index = split_morgue_file.index(x) + 3
        end_index = split_morgue_file.index(y) - 2
        return [spell.lstrip() for spell in split_morgue_file[start_index:end_index]]

        # return "13/15 runes: decaying, serpentine, slimy, silver, golden, iron, obsidian, icy, bone, abyssal, demonic, glowing, fiery"

    def runes(self):
        rune_regex = "(\d+\/\d+) runes: (.*(\n.*)?)\na:\s+"

        m = re.search(rune_regex, self.morgue_file)
        if m:
            return m.group(2).strip()

    # ========================================================================================

    def fetch_user_stats(self):
        # HP:   198/198 (201) AC: 49    Str: 39    XL:     25
        # Health: 192/192    AC: 25    Str: 21    XL:     27
        user_stats_regex = "[Health|HP]:(.*)AC:(.*)Str:(.*)XL:(.*)"
        m = re.search(user_stats_regex, self.morgue_file)
        if m:
            return {
                "health": m.group(1),
                "ac": m.group(2),
                "str": m.group(3),
                "xl": m.group(4),
            }

    def fetch_location(self):
        m = re.search(f"You are (in|on) (.*)", str(self.morgue_file))
        if m:
            return m.group(2)
