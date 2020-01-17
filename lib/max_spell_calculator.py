from lib.skill_factory import SkillFactory


class MaxSpellCalculator:
    def __init__(self, character):
        self.character = character
        # If we consume the generator properly
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
                (self.character.spellcasting() / 2)
                + (2 * self._average_spell_schools())
                + self._brilliance()
            )
            * self.enhancers()
            * (self.intelligence() / 10)
            * self.wild_magic()
            * self.augmentation()
        )

    # Average spell schools is the average of all the skills necessary for the spell -
    # up to three schools for some spells (e.g. Mephitic Cloud,
    # which requires Conjurations, Poison Magic, and Air Magic).
    def _average_spell_schools(self):
        spell_schools = self.spell.schools()
        total_skills = 0
        for spell_school in spell_schools:
            skill = self.character.lookup_skill(spell_school)
            total_skills = total_skills + skill.level
        return total_skills / len(spell_schools)

    # The boost is equal to three average skill levels,
    # but is still applied even if your average skill level has reached the max of 27.
    def _brilliance(self):
        return 0

    # Enhancers is a factor calculated from rings of fire, staves of cold,
    # a robe of the Archmagi, etc. You get +1 for every enhancer and -1 for every dampener.
    # If the factor is positive, your spell power is multiplied by 1.5(factor).
    # If it is negative, it is multiplied by 0.5(factor),
    # effectively halving your power every dampener. The factor is capped at ±3.
    def enhancers(self):
        # Do you have rings of fire, staves of cold, robe of Archmagi?
        # What are other enhancers
        return 1

    def intelligence(self):
        return self.character.intelligence()

    # Wild Magic is a mutation that increases your spell power,
    # but decreases your success rate. The bonus is ×1.3, ×1.6 or ×1.9
    # depending on how many levels of this mutation you have.
    def wild_magic(self):
        return 1

    # Augmentation is a demonspawn mutation which increases your spell power
    # and gives a slaying bonus at high HP. The spellpower bonus is ×1.4,
    # ×1.8 or ×2.2 depending on how much augmentation bonus you have.
    def augmentation(self):
        return 1
