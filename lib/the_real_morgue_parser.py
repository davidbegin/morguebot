class MorgueParser:
    def __init__(self, morgue_file):
        self.morgue_file = morgue_file

    def spells(self):
        x = "Your spell library contains the following spells:"
        y = "Dungeon Overview and Level Annotations"
        split_morgue_file = self.morgue_file.split("\n")
        start_index = split_morgue_file.index(x) + 3
        end_index = split_morgue_file.index(y) - 2
        return [spell.lstrip() for spell in split_morgue_file[start_index:end_index]]
