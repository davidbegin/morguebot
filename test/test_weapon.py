import pytest

from lib.weapon import Weapon
from lib.character import Character


def test_weapon():
    full_name = "the +9 sword of Zonguldrok (weapon) {reap}"
    name = "long sword"
    enchantment = 9
    character = Character(character="artmatt")

    subject = Weapon(
        full_name=full_name, name=name, enchantment=enchantment, character=character
    )

    assert subject.max_damage() == 18.04


def test_initializing_an_invalid_weapon_type():
    character = Character(character="artmatt")

    with pytest.raises(KeyError) as exc:
        full_name = "Not a real +0 weapon"
        Weapon(full_name=full_name, name="fake", enchantment=0, character=character)
    exception_msg = exc.value.args[0]
    assert exception_msg == f"Error Looking Up Weapon Type: {full_name}, fake"


# @pytest.fixture
# def morgue_file():
#     morgue_file_path = "Support/GucciMane.txt"
#     return open(morgue_file_path).read()


# def test_max_damage(morgue_file):
#     weapon_info = {"name": "long sword", "modifier": 5}
#     result = calc_max_damage(weapon_info, morgue_file)
#     assert result == 9.85
