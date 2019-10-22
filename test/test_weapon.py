import pytest

from lib.weapon import Weapon
from lib.character import Character

# @pytest.mark.focus
def test_weapon():
    full_name = "the +9 sword of Zonguldrok (weapon) {reap}"
    name = "long sword"
    enchantment = 9
    character = Character(character="artmatt")

    subject = Weapon(
        full_name=full_name, name=name, enchantment=enchantment, character=character
    )

    assert subject.max_damage() == 18.04
