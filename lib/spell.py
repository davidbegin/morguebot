class Spell:
    ABBREVIATIONS = {
        "Fire": "Fire Magic",
        "Tmut": "Transmutations",
        "Pois": "Poison Magic",
    }

    def __init__(self, name, spell_type, power, failure, level, hunger):
        self.name = name
        self.spell_type = spell_type
        self.power = power
        self.failure = failure
        self.level = level
        self.hunger = hunger

    def to_dir(self):
        return {
            "name": self.name,
            "spell_type": self.spell_type,
            "power": self.power,
            "failure": self.failure,
            "level": self.level,
            "hunger": self.hunger,
        }

    def at_least_level(self, desired_level):
        return self.level >= desired_level

    def overview(self):
        return f"{self.name} {self.spell_type} {self.power} {self.failure} {self.level} {self.hunger}"

    def schools(self):
        return [self.ABBREVIATIONS[school] for school in self.spell_type.split("/")]
