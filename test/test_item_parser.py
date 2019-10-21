import pytest

from lib.item_parser import parse_weapon


def test_parse_weapon():
    # 'the +8 storm bow {elec, penet}'
    # the +8 morningstar "Aho Hol" (weapon) {flame, rC++}
    weapon_input = "a +7 blowgun"
    result = parse_weapon(weapon_input)
    expected = {"name": weapon_name, "modifier": modifier}
