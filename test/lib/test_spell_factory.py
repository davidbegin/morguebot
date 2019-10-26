import pytest
from lib.spell_factory import SpellFactory


@pytest.mark.focus
def test_spell_factory_is_real():
    raw_spell = "Animate Skeleton  Necr  N/A  98%  1   ##....."
    spell = SpellFactory(raw_spell).new()

    assert spell.name == "Animate Skeleton"
    assert spell.spell_type == "Necr"
    assert spell.power == "N/A"
    assert spell.failure == "98%"
    assert spell.level == 1
    assert spell.hunger == "##....."
