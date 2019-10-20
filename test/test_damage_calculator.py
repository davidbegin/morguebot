import random
import pytest

from lib.damage_calculator import max_damage

from unittest.mock import patch
from unittest.mock import MagicMock

import lib.damage_calculator


@pytest.mark.parametrize(
    "weapon_info,character_info, expected",
    [
        ({"name": "long sword", "modifier": 9}, {"str": 5}, 18.53846153846154),
        # ({"type": "short sword", "modifier": -5}, 1),
    ],
)
def test_max_damage(weapon_info, character_info, expected):
    # with patch('lib.dice') as MockClass:
    #     instance = MockClass.return_value
    #     instance.one_d.return_value = 20
    assert max_damage(character_info, weapon_info) == expected

