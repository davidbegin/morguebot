from lib.morgue_parser import fetch_strength

from lib.morgue_parser import fetch_skill
from lib.morgue_parser import fetch_skills
from lib.weapon_stats import WEAPON_STATS
from lib.dice import one_d


class Weapon:
    def __init__(self, full_name, name, enchantment, character):
        self.full_name = full_name
        self.name = name
        self.enchantment = enchantment
        self.character = character
        self.morgue_file = self.character.morgue_file()

        try:
            self.weapon_type = WEAPON_STATS[self.name]["type"]
        except Exception as e:
            # import pdb
            # pdb.set_trace()
            print(
                f"\033[031mError Looking Up Weapon Type: {full_name} | {self.name}\033[0m"
            )

    def max_damage(self):
        if self.enchantment is None:
            return 0
        else:
            return self.calc_max_damage()

    def calc_max_damage(self):
        base_damage = self.calc_base_damage()

        strength_enchantment = self.calc_strength_enchantment()

        weapon_skill_enchantment = self.calc_weapon_skill_enchantment()

        fighting_skill_enchantment = self.calc_fighting_enchantment()

        slaying_bonuses = self.calc_slay_bonuses()

        misc_enchantments = 0

        base_damage + self.enchantment + strength_enchantment

        max_damage = (
            (one_d(base_damage * strength_enchantment + 1) - 1)
            * weapon_skill_enchantment
            * fighting_skill_enchantment
            + misc_enchantments
            + slaying_bonuses
        )

        return round(max_damage, 2)
        # Damage = {[1d(Base damage * Strength enchantment +1)-1] * Weapon skill enchantment * Fighting enchantment + Misc enchantments + Slaying bonuses} * Final multipliers + Stabbing bonus - AC damage reduction[1]

    # Base damage:
    # Unarmed combat: 3 + UC (can be changed by some spells, see Unarmed combat)
    # Using a weapon: Base damage of the weapon
    # TODO: come back handle these no weapon jerks
    def calc_base_damage(self):
        if self.name in WEAPON_STATS:
            return WEAPON_STATS[self.name]["base_damage"]
        else:
            raise Exception(f"\033[31;1mUnknown Weapon: {self.name}\033[0m")

    # Strength enchantment:
    # If Strength > 10: (39+((1d(Strength-8)-1)*2))/39
    # If Strength < 10: (39-((1d(12-Strength)-1)*3))/39
    # If Strength = 10: 1
    def calc_strength_enchantment(self):
        strength = fetch_strength(self.morgue_file)
        if strength == 10:
            return 1
        if strength > 10:
            return (39 + ((one_d(strength - 8) - 1) * 2)) / 39
        elif strength < 10:
            return (39 - ((one_d(12 - strength) - 1) * 3)) / 39

    # Weapon skill enchantment: Multiply by [2499 + 1d(100 * weapon_skill +1)]/2500 (not applied to unarmed combat)
    def calc_weapon_skill_enchantment(self):
        weapon_skill = fetch_skill(self.morgue_file, self.weapon_type)
        return (2499 + one_d(100 * weapon_skill + 1)) / 2500

    # Fighting enchantment: Multiply by [3999 + 1d(100 * fighting_skill +1)]/4000
    def calc_fighting_enchantment(self):
        fighting_skill = fetch_skill(self.morgue_file, "Fighting")
        return (3999 + one_d(100 * fighting_skill + 1)) / 4000

    # Misc enchantments:
    # Might or Berserk: +1d10
    # If you are starving: -1d5 + 1 (bloodless vampires don't suffer this penalty)
    def calc_misc_enchantment(self):
        return 0

    # Slaying bonuses:
    # Effective enchantment = Weapon enchantment + Slaying bonus
    # If Eff. enchantment > 0: + 1d(1 + Eff. enchantment) - 1
    # If Eff. enchantment < 0: - 1d(1 - Eff. enchantment) + 1
    def calc_slay_bonuses(self):
        eff_enchantment = self.enchantment + 0

        if eff_enchantment > 0:
            return one_d(1 + eff_enchantment) - 1
        elif self.enchantment < 0:
            return -(one_d(1 - eff_enchantment) + 1)
        else:
            return 0

    # Final multipliers:
    # If it is an additional cleaving attack: Multiply by 0.7
    # Statue Form: Multiply by 1.5
    # Shadow Form: Multiply by 0.5
    # If the player has the Weak status effect: Multiply by 0.75
    def calc_final_multipliers(self):
        return 0

    # Stabbing bonus: See stabbing.
    def calc_stabbing_bonus(self):
        return 0

    # AC damage reduction: See AC.
    def calc_ac_damage_reduction(self):
        return 0
