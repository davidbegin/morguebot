import re
import requests
import sys
import time


# This Belongs at a different level of abstraction
def read_morgue_file(morgue_file_path, morgue_url):
    if morgue_file_path:
        with open(morgue_file_path) as morgue_file:
            return morgue_file.read()
    elif morgue_url:
        return fetch_online_morgue(morgue_url)
    else:
        username = "beginbot"
        morgue_url = f"http://crawl.akrasiac.org/rawdata/{username}/{username}.txt"
        return fetch_online_morgue(morgue_url)


def fetch_online_morgue(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"\033[031;1mCould not find the Character at {url}\033[0m")
        sys.exit()


# ========================================================================================

# TODO: Figure out how ot combine this with _extract_skills
def _extract_inventory(morgue_file, start_cat, end_cat):
    split_morgue_file = morgue_file.split("\n")
    start_index = split_morgue_file.index(start_cat) + 1
    end_index = split_morgue_file.index(end_cat) + 1
    return split_morgue_file[start_index:end_index]


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


def fetch_weapons(morgue_file):
    return _extract_inventory(morgue_file, "Hand Weapons", "Armour")


def fetch_jewellery(morgue_file):
    return _extract_inventory(morgue_file, "Jewellery", "Wands")


def fetch_scrolls(morgue_file):
    return _extract_inventory(morgue_file, "Scrolls", "Potions")


def fetch_potions(morgue_file):
    return _extract_inventory(morgue_file, "Potions", "Comestibles")


# Lots to Refactor
# ========================================================================================


def fetch_mutations(morgue_file):
    m = re.search(f"A:\s(.*)", str(morgue_file))

    if m:
        return m.group(1)


def fetch_stealth(morgue_file):
    m = re.search(f"Stlth\s+(..........)\s+(.*)", str(morgue_file))

    if m:
        return m.group(1)


def fetch_mr(morgue_file):
    m = re.search(f"MR\s+(.....)\s+(.*)", str(morgue_file))

    if m:
        return m.group(1)


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


def fetch_overview(morgue_file):
    m = re.search(f".* Turns:\s(.*)", str(morgue_file))
    if m:
        return m.group(0)
