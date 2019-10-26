class Spell:
    def __init__(self, name, spell_type, power, failure, level, hunger):
        self.name = name
        self.spell_type = spell_type
        self.power = power
        self.failure = failure
        self.level = level
        self.hunger = hunger

    def at_least_level(self, desired_level):
        return self.level >= desired_level
