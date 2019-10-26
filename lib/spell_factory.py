from lib.spell import Spell

# Character -> Has a Morgue File
# |
# v
# Morgue Parser
#   Cuts out the raw string of info for that item
# |
# v
# (Item) Factory
#   Takes a Raw String and converts to inputs to make the object
# |
# v
# (Item)
#   The Actual Item


class SpellFactory:
    def __init__(self, raw_spell):
        self.raw_spell = raw_spell

    def new(self):
        split_spell = self.raw_spell.split()
        split_spell.reverse()

        hunger, level, failure, power, spell_type, *name = split_spell
        name.reverse()
        return Spell(
            name=(" ".join(name)),
            spell_type=spell_type,
            power=power,
            failure=failure,
            level=float(level),
            hunger=hunger,
        )
