import pytest
from pytest_mock import mocker
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


def test_morgue_file_from_s3(mocker):
    character = Character(name="beginbot")
    mocker.patch.object(character, "s3_morgue_file")

    expected_morgue_file = "Cool Morgue file"
    character.s3_morgue_file.return_value = expected_morgue_file
    morgue_file = character.morgue_file()
    character.s3_morgue_file.assert_called()
    assert morgue_file == expected_morgue_file


def test_morgue_file_from_crawl_server(mocker):
    character = Character(name="beginbot")
    mocker.patch.object(character, "s3_morgue_file")
    mocker.patch.object(character, "fetch_online_morgue")

    expected_morgue_file = "Online Morgue"
    character.s3_morgue_file.return_value = None
    character.fetch_online_morgue.return_value = expected_morgue_file
    morgue_file = character.morgue_file()

    character.s3_morgue_file.assert_called()
    character.fetch_online_morgue.assert_called()
    assert morgue_file == expected_morgue_file
