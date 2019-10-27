from lib.morgue_stalker import fetch_characters
from lib.character import Character
from lib.the_real_morgue_parser import MorgueParser
from lib.morgue_db import MorgueDB


class RuneFetcher:
    def fetch(self):
        characters = fetch_characters()

        for character_name in characters:
            character = Character(name=character_name)
            morgue_db = MorgueDB(character_name)
            morgue_parser = MorgueParser(character.non_saved_morgue_file())
            runes = morgue_parser.runes()
            if runes:
                nice_runes = [rune.strip() for rune in runes.split(",")]
                print(f"\033[37mSaving {character_name}'s runes\033[0m")
                morgue_db.save_stuff("SS", "runes", nice_runes)
        # We are going to go through all characters
        # Fetch and Save Runes
        # Write a DynamoDB query for themost Runs
