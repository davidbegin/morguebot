import random
import pytest

from lib.damage_calculator import max_damage

from unittest.mock import patch
from unittest.mock import MagicMock

import lib.damage_calculator


@pytest.fixture
def morgue_file():
    morgue_file_path = "Support/GucciMane.txt"
    return open(morgue_file_path).read()


@pytest.mark.parametrize(
    "weapon_info,expected",
    [
        ({"name": "long sword", "modifier": 9}, 13.846153846153847),
        # ({"type": "short sword", "modifier": -5}, 1),
    ],
)
def test_max_damage(morgue_file, weapon_info, expected):
    # with patch('lib.dice') as MockClass:
    #     instance = MockClass.return_value
    #     instance.one_d.return_value = 20
    assert max_damage(morgue_file, weapon_info) == expected
