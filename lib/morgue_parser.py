import re
import sys
import time


# ========================================================================================


def fetch_spells(morgue_file):
    x = "Your spell library contains the following spells:"
    y = "Dungeon Overview and Level Annotations"
    split_morgue_file = morgue_file.split("\n")
    start_index = split_morgue_file.index(x) + 3
    end_index = split_morgue_file.index(y) - 1
    return split_morgue_file[start_index:end_index]


# TODO: Figure out how ot combine this with _extract_skills
def _extract_inventory(morgue_file, start_cat, end_cat):
    try:
        split_morgue_file = morgue_file.split("\n")
        start_index = split_morgue_file.index(start_cat) + 1
        end_index = split_morgue_file.index(end_cat) + 1
        return split_morgue_file[start_index:end_index]
    except:
        return None


def _extract_skills(morgue_file, start_cat, end_cat):
    split_morgue_file = morgue_file.split("\n")
    start_index = split_morgue_file.index(start_cat) + 1
    end_index = split_morgue_file.index(end_cat, start_index)
    return split_morgue_file[start_index:end_index]


def fetch_altars(morgue_file):
    split_morgue_file = morgue_file.split("\n")
    start_index = split_morgue_file.index("Altars:") + 1
    end_index = split_morgue_file.index("", start_index)
    return split_morgue_file[start_index:end_index]


# ========================================================================================


def fetch_skills(morgue_file):
    return _extract_skills(morgue_file, "   Skills:", "")


def fetch_armour(morgue_file):
    return _extract_inventory(morgue_file, "Armour", "Jewellery")


def fetch_skill(morgue_file, skill):
    m = re.search(f"[\+\-\*] Level (.*) {skill}", morgue_file)

    if m:
        if "(" in m.group(1):
            return float(m.group(1).split("(")[0])
        else:
            return float(m.group(1))
    else:
        return 0


def fetch_weapon(morgue_file):
    weapons = fetch_weapons(morgue_file)
    for weapon in weapons:
        if "(weapon)":
            return weapon


def fetch_weapons(morgue_file):
    raw_weapons = _extract_inventory(morgue_file, "Hand Weapons", "Missiles")

    if raw_weapons is None:
        raw_weapons = _extract_inventory(morgue_file, "Hand Weapons", "Armour")

    if raw_weapons is None:
        return []

    formatted_weapons = []
    for weapon in raw_weapons:
        m = re.search(f"[a-zA-Z]\s+-\s+(.*)", weapon)
        if m:
            formatted_weapons.append(m.group(1))

    return formatted_weapons


def fetch_jewellery(morgue_file):
    return _extract_inventory(morgue_file, "Jewellery", "Wands")


def fetch_scrolls(morgue_file):
    return _extract_inventory(morgue_file, "Scrolls", "Potions")


def fetch_potions(morgue_file):
    return _extract_inventory(morgue_file, "Potions", "Comestibles")


# Lots to Refactor
# ========================================================================================


def fetch_stealth(morgue_file):
    m = re.search(f"Stlth\s+(..........)\s+(.*)", str(morgue_file))

    if m:
        return m.group(1)


def fetch_mr(morgue_file):
    m = re.search(f"MR\s+(.....)\s+(.*)", str(morgue_file))

    if m:
        return m.group(1)


def fetch_strength(morgue_file):
    user_stats = fetch_user_stats(morgue_file)
    raw_strength = user_stats["str"].strip()
    return int(raw_strength.split()[0])


def fetch_user_stats(morgue_file):
    # HP:   198/198 (201) AC: 49    Str: 39    XL:     25
    # Health: 192/192    AC: 25    Str: 21    XL:     27
    user_stats_regex = "[Health|HP]:(.*)AC:(.*)Str:(.*)XL:(.*)"
    m = re.search(user_stats_regex, morgue_file)
    if m:
        return {
            "health": m.group(1),
            "ac": m.group(2),
            "str": m.group(3),
            "xl": m.group(4),
        }


# ========================================================================================


def fetch_trait(morgue_file, trait):
    m = re.search(f"r\w+\s+.\s.\s.\s+({trait})\s+(.)\s+(.*)", str(morgue_file))

    if m:
        trait_name = m.group(1)
        trait_value = m.group(2)
        return trait_value


def fetch_resistance(morgue_file, resistance):
    m = re.search(f"({resistance})\s+(. . .)\s+(\w+)\s+(.*)", str(morgue_file))

    if m:
        resistance_name = m.group(1)
        resistance_value = m.group(2)
        return resistance_value


# ========================================================================================


def fetch_health(morgue_file):
    m = re.search(
        f"Health:\s+(.*)AC:\s+(.*)Str:\s+(.*)XL:\s+(.*)\s+Next:\s+(.*)",
        str(morgue_file),
    )
    if m:
        return m.group(1)


def fetch_xl_level(morgue_file):
    m = re.search(
        f"Health:\s+(.*)AC:\s+(.*)Str:\s+(.*)XL:\s+(.*)\s+Next:\s+(.*)",
        str(morgue_file),
    )
    if m:
        return m.group(4)


def fetch_seed(morgue_file):
    m = re.search(f"Game seed:\s(.*)", str(morgue_file))
    if m:
        return m.group(0)


def fetch_turns(morgue_file):
    m = re.search(f".* Turns:\s(.*),.*", str(morgue_file))
    if m:
        return m.group(1)


def fetch_overview(morgue_file):
    user_stats = fetch_user_stats(morgue_file)
    xl_level = user_stats["xl"]
    health = user_stats["health"]

    location = fetch_location(morgue_file)

    m = re.search(f"(.*) Turns:\s(.*)", str(morgue_file))
    if m:
        return f"{m.group(1).strip()}  XL: {xl_level}  Health: {health}  Location: {location}".strip()


def fetch_location(morgue_file):
    m = re.search(f"You are on (.*)", str(morgue_file))
    if m:
        return m.group(1)


def fetch_god(morgue_file):
    # You worship Vehumet.
    pass
