class MaxSpellCalculator:
    def __init__(self, character):
        self.character = character
        self.spells = character.spells()

    def calculate(self):
        return [
            SpellCalculator(character=self.character, spell=spell).max_power()
            for spell in self.spells
        ]


class SpellCalculator:
    def __init__(self, character, spell):
        self.character = character
        self.spell = spell

    def max_power(self):
        return (
            (
                (self.spellcasting() / 2)
                + (2 * self.average_spell_schools())
                + self.brilliance()
            )
            * self.enhancers()
            * (self.intelligence() / 10)
            * self.wild_magic()
            * self.augmentation()
        )

    def spellcasting(self):
        return self.character.spellcasting()

    # Average spell schools is the average of all the skills necessary for the spell -
    # up to three schools for some spells (e.g. Mephitic Cloud, which requires Conjurations, Poison Magic, and Air Magic).
    def average_spell_schools(self):
        spell_schools = self.spell.schools()
        total_skills = 0
        for spell_school in spell_schools:
            total_skills += self.character.lookup_skill(spell_school)
        return total_skills / len(spell_school)

    def brilliance(self):
        return 1

    def enhancers(self):
        return 1

    def intelligence(self):
        return 1

    def wild_magic(self):
        return 1

    def augmentation(self):
        return 1
