import pytest

from lib.damage_calculator import max_damage


@pytest.mark.parametrize(
    "weapon_info,character_info, expected",
    [
        ({"type": "long sword", "modifier": 9}, {"str": 5}, 18),
        # ({"type": "short sword", "modifier": -5}, 1),
    ],
)
def test_max_damage(weapon_info, character_info, expected):
    assert max_damage(character_info, weapon_info) == expected
