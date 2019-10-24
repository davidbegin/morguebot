import pytest
from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_resistance
from lib.morgue_parser import fetch_trait
from lib.morgue_parser import fetch_mr
from lib.morgue_parser import fetch_altars
from lib.morgue_parser import fetch_strength
from lib.morgue_parser import fetch_skill
from lib.morgue_parser import fetch_weapon

from lib.character import Character


@pytest.fixture
def morgue_file():
    morgue_file_path = "Support/GucciMane.txt"
    return open(morgue_file_path).read()


def test_fetch_strength(morgue_file):
    assert fetch_strength(morgue_file) == 5


def test_fetch_weapon(morgue_file):
    weapon = fetch_weapon(morgue_file)
    assert weapon == "a +0 dagger of venom (weapon)"


@pytest.mark.parametrize(
    "weapon_type,expected", [("Conjurations", 4.6), ("Long Blades", 0)]
)
def test_fetch_weapon_skill(morgue_file, weapon_type, expected):
    weapon_skill = fetch_skill(morgue_file, weapon_type)
    assert weapon_skill == expected


def test_morgue_parser_altar_finding(morgue_file):
    pass


def test_morgue_parser_overview(morgue_file):
    character = Character(name="None")
    overview = fetch_overview(character.morgue_file())
    expected_overview = "None the Carver (Minotaur Gladiator)  XL:      11   Next: 58%  Health:  102/102      Location: level 2 of the Lair of Beasts."
    assert overview == expected_overview


def test_morgue_parser_resistance(morgue_file):
    expected_output = ". . ."
    assert fetch_resistance(morgue_file, "rFire") == expected_output


def test_morgue_parser_traits(morgue_file):
    expected_output = "."
    assert fetch_trait(morgue_file, "SeeInvis") == expected_output


def test_morgue_parser_mr(morgue_file):
    expected_output = "....."
    assert fetch_mr(morgue_file) == expected_output
