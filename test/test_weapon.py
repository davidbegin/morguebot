import pytest

from lib.weapon import Weapon
from lib.character import Character


@pytest.mark.focus
def test_weapon():
    full_name = "the +9 sword of Zonguldrok (weapon) {reap}"
    name = "long sword"

    enchantment = 9
    character = Character(morgue_filepath="support/GucciMane.txt")

    subject = Weapon(
        full_name=full_name, name=name, enchantment=enchantment, character=character
    )

    assert subject.max_damage() == 39.07


def test_initializing_an_invalid_weapon_type():
    character = Character(morgue_filepath="support/GucciMane.txt")

    with pytest.raises(KeyError) as exc:
        full_name = "Not a real +0 weapon"
        Weapon(full_name=full_name, name="fake", enchantment=0, character=character)
    exception_msg = exc.value.args[0]
    assert exception_msg == f"Error Looking Up Weapon Type: {full_name}, fake"
