from lib.weapon_factory import WeaponFactory

# Weapons Appraisers have a deep relationship with thier patrons
class WeaponsAppraiser:
    def __init__(self, character, weapons):
        self.character = character
        self.weapons = weapons

    # This returns the max damages for all weapons
    def calc_max_damages(self):
        if not self.weapons:
            return ["No Weapons Found!"]
        else:
            max_damages = self._find_max_damages()

            if max_damages:
                return max_damages

    def _find_max_damages(self):
        max_damages = []
        for weapon in self.weapons:
            weapon = WeaponFactory.new(self.character, weapon)
            max_damage = weapon.max_damage()

            # TODO: Come back and handle telling people about unidentified weapons
            if max_damage:
                max_damages.append(
                    {
                        "weapon": weapon.full_name,
                        "max_damage": max_damage,
                        "type": weapon.weapon_type,
                        "character": self.character.name,
                    }
                )

        def sort_by_max_damage(elem):
            return elem["max_damage"]

        max_damages.sort(key=sort_by_max_damage)

        return max_damages
