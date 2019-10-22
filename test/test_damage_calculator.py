import random
import pytest

from lib.damage_calculator import calc_max_damage

from unittest.mock import patch
from unittest.mock import MagicMock

import lib.damage_calculator


@pytest.fixture
def morgue_file():
    morgue_file_path = "Support/GucciMane.txt"
    return open(morgue_file_path).read()


def test_max_damage(morgue_file):
    weapon_info = {"name": "long sword", "modifier": 5}
    result = calc_max_damage(weapon_info, morgue_file)
    assert result == 9.85
