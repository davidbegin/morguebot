import boto3

from lib.morgue_parser import fetch_altars


def validate_seed(character):
    pass
    # old_seed = _fetch_seed(character.character)

    # if old_seed != character.seed:
    #     print("New Seeds!")
    #     _store_seed(character.character, character.seed)


# Fun Fact: There are currently 25 gods in DC
def check_for_new_gods(character, printer):
    old_altars = _fetch_gods(character.character)
    altars = set(fetch_altars(character.morgue_file()))

    print(f"old_altars: {old_altars}")
    print(f"altars: {altars}")

    if len(altars) > len(old_altars):
        new_altars = altars.difference(set(old_altars))
        print(f"We Found a new God(s): {new_altars}")
        printer.print_missionary(new_altars)

    if len(altars) > 0:
        _store_gods(character.character, list(altars))
