import pytest
from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_resistance
from lib.morgue_parser import fetch_trait
from lib.morgue_parser import fetch_mr
from lib.morgue_parser import fetch_altars
from lib.morgue_parser import parse_weapon
from lib.morgue_parser import fetch_strength
from lib.morgue_parser import fetch_weapon_skill

from lib.damage_calculator import max_damage

from lib.character import Character


@pytest.fixture
def morgue_file():
    morgue_file_path = "Support/GucciMane.txt"
    return open(morgue_file_path).read()


# "a +9 dagger of speed"
# "a +3 antimagic broad axe"
@pytest.mark.parametrize(
    "weapon,expected",
    [
        (
            "the +9 sword of Zonguldrok (weapon) {reap}",
            {"name": "long sword", "modifier": 9},
        ),
        ("the -5 short sword of Begin {slay}", {"name": "short sword", "modifier": -5}),
    ],
)
def test_parsing_weapons(weapon, expected):
    assert parse_weapon(weapon) == expected


def test_fetch_strength(morgue_file):
    assert fetch_strength(morgue_file) == 5


def test_fetch_weapon_skill(morgue_file):
    weapon_type = "Conjurations"
    weapon_skill = fetch_weapon_skill(morgue_file, weapon_type)
    assert weapon_skill == 4.6


def test_morgue_parser_altar_finding(morgue_file):
    pass


def test_morgue_parser_overview(morgue_file):
    character = Character(character="None")
    overview = fetch_overview(character.morgue_file())
    expected_overview = "None the Carver (Minotaur Gladiator)  XL: 11    Health: 102/102      Location: level 2 of the Lair of Beasts."
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
