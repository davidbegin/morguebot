import pytest
from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_resistance
from lib.morgue_parser import fetch_trait
from lib.morgue_parser import fetch_mr
from lib.morgue_parser import fetch_altars


# HOW do you let fixtures take arguments?


@pytest.fixture
def morgue_file():
    morgue_file_path = "Support/GucciMane.txt"
    return open(morgue_file_path).read()


def test_morgue_parser_altar_finding(morgue_file):
    expected_altars = [
        "Ashenzari",
        "Cheibriados",
        "Dithmenos",
        "Elyvilon",
        "Fedhas",
        "Gozag",
        "Hepliaklqana",
        "Kikubaaqudgha",
        "Makhleb",
        "Nemelex Xobeh",
        "Okawaru",
        "Qazlal",
        "Ru",
        "Sif Muna",
        "Trog",
        "Uskayaw",
        "Vehumet",
        "Wu Jian",
        "Xom",
        "Yredelemnul",
        "The Shining One",
    ]
    morgue_file = open("Support/WilliamGates.txt").read()
    altars = fetch_altars(morgue_file)
    assert altars == expected_altars


def test_morgue_parser_overview(morgue_file):
    expected_overview = "Gucci Mane the Conjurer (Deep Elf Conjurer)          Turns: 737, Time: 00:02:30"
    assert fetch_overview(morgue_file) == expected_overview


def test_morgue_parser_resistance(morgue_file):
    expected_output = ". . ."
    assert fetch_resistance(morgue_file, "rFire") == expected_output


def test_morgue_parser_traits(morgue_file):
    expected_output = "."
    assert fetch_trait(morgue_file, "SeeInvis") == expected_output


def test_morgue_parser_mr(morgue_file):
    expected_output = "....."
    assert fetch_mr(morgue_file) == expected_output
