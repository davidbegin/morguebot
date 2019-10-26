import pytest
from lib.spell import Spell

# Show me Spells above level X
def test_spell_is_real():
    spell = Spell(
        name="Animate Skeleton",
        spell_type="Necr",
        power="N/A",
        failure="98%",
        level=1,
        hunger="##.....",
    )


@pytest.mark.focus
def test_spell_at_least_level_3():
    spell = Spell(
        name="Animate Skeleton",
        spell_type="Necr",
        power="N/A",
        failure="98%",
        level=3,
        hunger="##.....",
    )

    assert spell.at_least_level(3)
