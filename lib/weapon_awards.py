from lib.morgue_stalker import fetch_characters
from lib.character import Character
from lib.kinesis import send_chat_to_stream

from lib.weapons_formatter import WeaponsFormatter
from lib.weapons_appraiser import WeaponsAppraiser
from lib.morgue_parser import fetch_weapons


def find_the_max_damage_for_all_characters():
    characters = fetch_characters()

    most_powerful_weapon = {"max_damage": 0}

    all_max_damages = []
    for character_name in characters:
        character = Character(name=character_name)
        weapons = fetch_weapons(character.morgue_file())

        weapons_appraiser = WeaponsAppraiser(character=character, weapons=weapons)
        max_damages = weapons_appraiser.calc_max_damages()

        # max_damages = character.calc_max_damages()

        if max_damages == ["No Weapons Found!"]:
            print(
                f"\033[37mIt's ok get some weapons and come back: {character_name}\033[0m"
            )
        else:
            all_max_damages.extend(max_damages)

    max_by_type = find_max_by_type(all_max_damages)

    send_chat_to_stream(["PorscheWIN Third Annual Weapon Awards!!! PorscheWIN"])

    for weapon_info in max_by_type:
        emoji = find_emoji(weapon_info["type"])
        send_chat_to_stream(
            [
                f"{emoji} Winner {weapon_info['character']} {emoji} - Category: {weapon_info['type']}",
                # f"Kreygasm Winner {weapon_info['character']} Kreygasm - Category: {weapon_info['type']}",
                WeaponsFormatter(character, []).format_weapon(weapon_info)
                # f"{weapon_info['weapon']} - {weapon_info['max_damage']}",
            ]
        )


# ========================================================================================


def find_emoji(category):
    emoji_map = {
        "Short Blades": "🗡",
        "Long Blades": "⚔",
        "Axes": "🌲",
        "Polearms": "🖌",
        "Maces & Flails": "⚒",
        "Throwing": "🤽",
        "Staves": "🚏",
        "Crossbows": "🏹 🏹",
        "Bows": "🏹",
        "Slings": "🤹",
    }
    return emoji_map.get(category, "Kreygasm")


def sort_by_max_damage(elem):
    return elem["max_damage"]


def find_max_by_type(max_damages):
    # {'weapon': 'a +3 dagger of speed (weapon)', 'max_damage': 9.25, 'type': 'Short Blades'}
    types = set([weapon_info["type"] for weapon_info in max_damages])

    most_powerful_weapons = []

    for weapon_type in types:
        weapons = [
            weapon_info
            for weapon_info in max_damages
            if weapon_info["type"] == weapon_type
        ]
        weapons.sort(key=sort_by_max_damage)
        # weapons.sort(key=lambda: elem: elem["max_damage"])
        weapons[-1].update({"score": len(weapons)})
        most_powerful_weapons.append(weapons[-1])

    return most_powerful_weapons
