import pytest
from lib.character import Character
from lib.spell import Spell


def test_morgue_filepath():
    local_mode = True
    character = Character(name="GucciMane", local_mode=local_mode)
    expected_filepath = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/GucciMane.txt"
    assert character.morgue_filepath == expected_filepath


def test_morgue_url():
    character = Character(name="GucciMane")
    expected_url = "http://crawl.akrasiac.org/rawdata/GucciMane/GucciMane.txt"
    assert character.morgue_url == expected_url


def test_spells():
    character = Character(name="GucciMane", local_mode=True)
    spells = character.spells()
    assert type(spells[0]) == Spell
    # This should return Spell objects


@pytest.mark.focus
def test_spells_above():
    character = Character(name="GucciMane", local_mode=True)
    spells = character.spells_above(4)
    expected_spells = [
        "Poison Arrow Conj/Pois #######... 1% 6.0 None",
        "Throw Icicle Conj/Ice ######.. 1% 4.0 None",
        "Yara's Violent Unravell Hex/Tmut ######.... 4% 5.0 None",
        "Invisibility Hex ######.. 14% 6.0 None",
        "Metabolic Englaciation Hex/Ice ######.... 17% 5.0 None",
        "Alistair's Intoxication Tmut/Pois #####... 24% 5.0 None",
        "Petrify Tmut/Erth ####.... 38% 4.0 None",
    ]
    assert spells == expected_spells
