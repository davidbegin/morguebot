import os
import re
import time
from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_resistance
from lib.morgue_parser import fetch_trait
from lib.morgue_parser import fetch_mr
from lib.morgue_parser import fetch_stealth
from lib.morgue_parser import fetch_mutations
from lib.morgue_parser import fetch_jewellery
from lib.morgue_parser import fetch_scrolls
from lib.morgue_parser import fetch_potions
from lib.morgue_parser import fetch_weapons
from lib.morgue_parser import fetch_armour
from lib.morgue_parser import fetch_skills
from lib.morgue_parser import fetch_altars


# I Need a better data struct for aliases
ALIASES = {"rF": "rFire", "rE": "rElec", "rC": "rCold", "rP": "rPois", "MR": "TODO"}


# TODO: The Printer does too much!!!
# It fetches everything!
# it should be instansiated with a morgue_file,
# or continually updated


class Printer:
    def __init__(self, server, disable_twitch=False, character=None):
        self.server = server
        self.disable_twitch = disable_twitch
        self.character = character

    def find_aliases(name):
        pass

    # This Belongs somewhere else
    def _find_resistance(self, resistance_type, items):
        resistance_type_aliases = find_aliases(resistance_type)
        return [item for item in items if ("rF+" in item or "rFire" in item)]

    # This is too much logic for here also
    def print_max_resistance(self, morgue_file):
        resistance_type = "rFire"

        # This will get complicated, with character limitations
        # Weapon to Shield

        # what weapon has the most Rf
        weapons = fetch_weapons(morgue_file)
        armour = fetch_armour(morgue_file)
        mutations = fetch_mutations(morgue_file)
        jewellery = fetch_jewellery(morgue_file)

        w = self._find_resistance(resistance_type, weapons)
        a = self._find_resistance(resistance_type, armour)
        m = self._find_resistance(resistance_type, mutations)
        j = self._find_resistance(resistance_type, jewellery)

        all_resistant_items = w + a + m + j
        print(all_resistant_items)

        self.send_msg(f"SeriousSloth All {resistance_type} Items SeriousSloth")
        self.sleep()
        for item in all_resistant_items:
            self.send_msg(item)
            self.sleep()

    # THIs belongs at a different level of abstraction
    def send_msg(self, msg):
        if not self.disable_twitch:
            # TODO: Make this configurable
            channel = "#beginbot"

            if msg:
                self.server.send(
                    bytes("PRIVMSG " + channel + " :" + msg + "\n", "utf-8")
                )

    def print_command(self, name, value):
        fmt_str = f"{name}: {value}"
        print("\n\033[35m" + fmt_str + "\033[0m")
        self.send_msg(fmt_str)

    def print_gods(self, morgue_file):
        altars = set(fetch_altars(morgue_file))
        gods_remaining = 25 - len(altars)

        if len(altars) == 25:
            self.send_msg("Kreygasm YOU HAVE SEEN EVERY GOD! Kreygasm")
        else:
            self.send_msg(f"MercyWing1 Gods MercyWing2")
            self.send_msg(", ".join(sorted(altars)))
            self.send_msg(f"You have {gods_remaining} to be found")

    def print_skills(self, morgue_file):
        self.send_msg(f"PowerUpL Listing All Skills PowerUpR")
        skills = fetch_skills(morgue_file)
        self.sleep()

        for skill in skills:
            split_skills = skill.split()
            if len(split_skills) == 3:
                _, level, *skill = skill.split()
            else:
                _, _, level, *skill = skill.split()

            msg = f"Level {level} {' '.join(skill)}"
            print(msg)
            self.send_msg(msg)
            self.sleep()

    def print_stealth(self, morgue_file):
        self.print_command("Stealth", fetch_stealth(morgue_file))

    def print_mr(self, morgue_file):
        self.print_command("Magic Resistance", fetch_mr(morgue_file))

    # ========================================================================================

    def print_traits(self, trait_type, morgue_file):
        trait = fetch_trait(morgue_file, trait_type[1:])

        if trait:
            trait_str = f"{trait_type[1:]}:   {trait}"
            print("\n\033[35m" + trait_str + "\033[0m")
            self.send_msg(trait_str)
        else:
            print("\n\033[35m" + "No TRAIT FOUND! " + "\033[0m")

    def print_resistance(self, resistance_type, morgue_file):
        if ALIASES.get(resistance_type, None):
            resistance = fetch_resistance(morgue_file, ALIASES[resistance_type])
        else:
            resistance = fetch_resistance(morgue_file, resistance_type)

        if resistance:
            resistance_str = f"{resistance_type}:   {resistance}"
            print("\n\033[35m" + resistance_str + "\033[0m")
            self.send_msg(resistance_str)
        else:
            print("\n\033[35m" + "No Resistance FOUND! " + "\033[0m")

    # ========================================================================================

    def print_overview(self, morgue_file):
        overview = fetch_overview(morgue_file)
        print("\n\033[35m" + str(overview) + "\033[0m")
        self.send_msg(overview)

    def print_mutations(self, morgue_file):
        self.send_msg(f"Squid1 Squid2 Listing All Mutations Squid4")
        self.sleep()
        self.print_command("Mutations", fetch_mutations(morgue_file))

    def print_missionary(self, new_altars):
        self.send_msg(f"MercyWing1 New Gods! MercyWing2")
        self.sleep()
        self.send_msg(", ".join(new_altars))

    def print_help(self, commands):
        self.send_msg(f"TheIlluminati Valid Commands: TheIlluminati")
        self.sleep()
        self.send_msg(", ".join(commands))

    # ========================================================================================

    def print_unique_items(self, morgue_file, title, items, regex):
        self.send_msg(title)
        self.sleep()

        for item in items:
            m = re.search(regex, item)
            if m:

                # This should check for the amout of groups to know whether it has amounts
                msg = m.group(1)
                print(msg)
                self.send_msg(msg)
            self.sleep()

    def print_weapons(self, morgue_file):
        self.print_unique_items(
            morgue_file,
            f"twitchRaid Listing All Weapons twitchRaid",
            fetch_weapons(morgue_file),
            f"\w\s-\s(.*)",
        )

    def print_armour(self, morgue_file):
        self.print_unique_items(
            morgue_file,
            f"BloodTrail Listing All Armour BloodTrail",
            fetch_armour(morgue_file),
            f"\w\s-\s(.*)",
        )

    def print_jewellery(self, morgue_file):
        self.print_unique_items(
            morgue_file,
            f"CoolCat Listing All Jewellery CoolCat",
            fetch_jewellery(morgue_file),
            f"\w\s-\s(.*)",
        )

    # ========================================================================================

    # TODO: combing the capture into, or branch on amout
    def print_potions(self, morgue_file):
        self.send_msg(f"DrinkPurple Listing All Potions DrinkPurple")
        potions = fetch_potions(morgue_file)
        self.sleep()

        for potion in potions:
            m = re.search(f"\w\s-\s(\d+)\s(.*)", potion)
            if m:
                amount = m.group(1)
                potion_name = m.group(2)
                msg = f"{amount} {potion_name}"
                print(msg)
                self.send_msg(msg)
            self.sleep()

    def print_scrolls(self, morgue_file):
        scrolls = fetch_scrolls(morgue_file)
        self.send_msg(f"copyThis Listing All Scrolls copyThis")
        self.sleep()

        for scroll in scrolls:
            m = re.search(f"\w\s-\s(\d+)\s(.*)", scroll)
            if m:
                amount = m.group(1)
                scroll_name = m.group(2)
                msg = f"{amount} {scroll_name}"
                print(msg)
                self.send_msg(msg)
            self.sleep()

    # ========================================================================================

    # Does This belong here
    def sleep(self):
        if not self.disable_twitch:
            time.sleep(1)
