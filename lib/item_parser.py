import re

from lib.weapon_stats import WEAPON_STATS


def parse_weapon(weapon):
    m = re.search(f"([-+]\d+)(.*)", weapon)

    if m:
        raw_modifier = m.group(1).strip()

        if raw_modifier.startswith("+"):
            modifier = int(raw_modifier[1:])
        else:
            modifier = int(raw_modifier)

        rest_of_the_weapon = m.group(2)

        weapon_name = None
        for weapon in WEAPON_STATS.keys():
            if weapon in rest_of_the_weapon:
                weapon_name = weapon

        if weapon_name is None:
            if "sword" in rest_of_the_weapon:
                weapon_name = "short sword"
            else:
                print(
                    f"\033[31;1mUnknown Weapon: {rest_of_the_weapon} | Modifier: {modifier}\033[0m"
                )
    else:
        modifier = None

    return {"name": weapon_name, "modifier": modifier}
