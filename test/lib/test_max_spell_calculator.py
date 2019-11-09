import pytest

from lib.character import Character
from lib.max_spell_calculator import MaxSpellCalculator
from lib.max_spell_calculator import SpellCalculator
from lib.spell_factory import SpellFactory


@pytest.mark.skip
def test_spell_calculator():
    character = Character(morgue_filepath="support/GucciMane.txt", local_mode=True)
    raw_spell = (
        "Ignite Poison            Fire/Tmut/Pois #######.     1%          3    None"
    )
    spell = SpellFactory(raw_spell).new()
    spell_calculator = SpellCalculator(character=character, spell=spell)
    result = spell_calculator.max_power()
    assert result == 0.275


@pytest.mark.skip
def test_average_spell_schools():
    # character = Character(morgue_filepath="support/GucciMane.txt", local_mode=True)
    # raw_spell = (
    #     "Ignite Poison            Fire/Tmut/Pois #######.     1%          3    None"
    # )
    # spell = SpellFactory(raw_spell).new()
    # spell_calculator = SpellCalculator(character=character, spell=spell)
    # result = spell_calculator._average_spell_schools()
    # assert result == 0

    character = Character(morgue_filepath="support/sunspire.txt", local_mode=True)
    raw_spell = (
        "Ignite Poison            Fire/Tmut/Pois #######.     1%          3    None"
    )
    spell = SpellFactory(raw_spell).new()
    spell_calculator = SpellCalculator(character=character, spell=spell)
    result = spell_calculator._average_spell_schools()
    assert result == 14.3


@pytest.mark.skip
def test_max_spell_calculator():
    # character = Character(morgue_filepath="support/sunspire.txt", local_mode=True)
    character = Character(morgue_filepath="support/GucciMane.txt", local_mode=True)
    max_spell_calculator = MaxSpellCalculator(character=character)
    result = max_spell_calculator.calculate()

    expected = [
        {
            "name": "Searing Ray",
            "spell_type": "Conj",
            "power": "###...",
            "failure": "3%",
            "level": 2.0,
            "hunger": "##.....",
        },
        {
            "name": "Dazzling Spray",
            "spell_type": "Conj/Hex",
            "power": "##....",
            "failure": "17%",
            "level": 3.0,
            "hunger": "###....",
        },
        {
            "name": "Iskenderun's Mystic Bla",
            "spell_type": "Conj",
            "power": "###.....",
            "failure": "22%",
            "level": 4.0,
            "hunger": "####...",
        },
        {
            "name": "Force Lance",
            "spell_type": "Conj/Tloc",
            "power": "##......",
            "failure": "50%",
            "level": 4.0,
            "hunger": "####...",
        },
        {
            "name": "Fulminant Prism",
            "spell_type": "Conj/Hex",
            "power": "##........",
            "failure": "50%",
            "level": 4.0,
            "hunger": "####...",
        },
    ]

    assert result == expected
