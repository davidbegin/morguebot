from lib.morgue_stalker import fetch_characters
from lib.character import Character
from lib.kinesis import send_chat_to_stream

from lib.weapons_formatter import WeaponsFormatter
from lib.weapons_appraiser import WeaponsAppraiser
from lib.morgue_parser import fetch_weapons

from lib.pawn_star import PawnStar


def celebrate_awards(max_by_type):
    send_chat_to_stream(["PorscheWIN Third Annual Weapon Awards!!! PorscheWIN"])
    for weapon_info in max_by_type:
        character = Character(name=weapon_info["character"])
        emoji = find_emoji(weapon_info["type"])

        pawn_star = PawnStar(weapon_info["weapon"])
        if pawn_star.is_unrand():
            unrand_emoji = "PraiseIt"
        else:
            unrand_emoji = ""

        send_chat_to_stream(
            [
                f"{emoji} {unrand_emoji} Winner {weapon_info['character']} {unrand_emoji} {emoji} - Category: {weapon_info['type']}",
                WeaponsFormatter(character, []).format_weapon(weapon_info),
            ]
        )


def find_the_max_damage_for_all_characters():
    characters = set(fetch_characters())

    all_max_damages = []
    for character_name in characters:
        print(f"\033[33mEntering {character_name} into the Weapon Awards...\033[0m")
        character = Character(name=character_name)
        weapons = fetch_weapons(character.morgue_file())

        weapons_appraiser = WeaponsAppraiser(character=character, weapons=weapons)
        max_damages = weapons_appraiser.calc_max_damages()

        if max_damages == ["No Weapons Found!"]:
            print(
                f"\033[37mIt's ok get some weapons and come back: {character_name}\033[0m"
            )
        else:
            all_max_damages.extend(max_damages)

    max_by_type = find_max_by_type(all_max_damages)
    celebrate_awards(max_by_type)


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
    types = set([weapon_info["type"] for weapon_info in max_damages])

    most_powerful_weapons = []

    for weapon_type in types:
        weapons = [
            weapon_info
            for weapon_info in max_damages
            if weapon_info["type"] == weapon_type
        ]
        weapons.sort(key=sort_by_max_damage)
        weapons[-1].update({"score": len(weapons)})
        most_powerful_weapons.append(weapons[-1])

    return most_powerful_weapons
