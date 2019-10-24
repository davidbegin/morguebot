from lib.morgue_stalker import fetch_characters
from lib.character import Character


# Go through every single character bucket
# Fetch their morgue file
# and if they don't have a morgue
# we are deleting their bucket
def clean_the_morgue():
    characters = fetch_characters()
    for character_name in characters:
        character = Character(name=character_name)
        morgue_url = character.morgue_url
        online_morgue = character._fetch_online_morgue()

        if "Escaped with the Orb" in online_morgue:
            import pdb

            pdb.set_trace()

        if online_morgue:
            print(f"You get to live: {character.name} {morgue_url}")
        else:
            print(f"\033[31;1mNO ONLINE MORGUE FOUND FOR: {character.name}\033[0m")
