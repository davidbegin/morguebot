from lib.morgue_stalker import fetch_characters
from lib.character import Character
from lib.kinesis import send_chat_to_stream



def find_the_max_damage_for_all_characters():
    characters = fetch_characters()

    most_powerful_weapon = {"max_damage": 0}

    all_max_damages = []
    for character_name in characters:
        character = Character(character=character_name)
        max_damages = character.calc_max_damages()
        if max_damages == ["No Weapons Found!"]:
            print(
                f"\033[37mIt's ok get some weapons and come back: {character_name}\033[0m"
            )
        else:
            all_max_damages.extend(max_damages)

    max_by_type = find_max_by_type(all_max_damages)

    send_chat_to_stream(["PorscheWIN Second Annual Weapon Awards!!! PorscheWIN"])
    for the_best in max_by_type:
        send_chat_to_stream(
            [
                f"Kreygasm Winner {the_best['character']} Kreygasm - Category: {the_best['type']}",
                f"{the_best['weapon']} - {the_best['max_damage']}",
            ]
        )


# ========================================================================================

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


