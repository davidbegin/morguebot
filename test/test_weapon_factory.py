import pytest

from lib.weapon_factory import WeaponFactory
from lib.character import Character

# "a +9 dagger of speed"
# "a +3 antimagic broad axe"
@pytest.mark.parametrize(
    "raw_weapon,name,enchantment,weapon_type",
    [
        ("the +9 sword of Zonguldrok (weapon) {reap}", "long sword", 9, "Long Blades"),
        ("a +7 blowgun", "blowgun", 7, "Throwing"),
        ("the -5 short sword of Begin {slay}", "short sword", -5, "Short Blades"),
        ("a +9 dagger of speed", "dagger", 9, "Short Blades"),
        ("a +3 antimagic broad axe", "broad axe", 3, "Axes"),
        (
            'the +14 lance "Wyrmbane" (weapon) {slay drac, rPois rF+ rC+ AC+3}',
            "spear",
            14,
            "Polearms",
        ),
        (
            'the +8 morningstar "Aho Hol" (weapon) {flame, rC++}',
            "morningstar",
            8,
            "Maces & Flails",
        ),
        ("the +7 Singing Sword {slice, sonic wave}", "long sword", 7, "Long Blades"),
    ],
)
@pytest.mark.focus
def test_creating_new_weapon(raw_weapon, name, enchantment, weapon_type):
    character = Character(character="beginbot")
    weapon = WeaponFactory.new(character, raw_weapon)

    assert weapon.name == name
    assert weapon.enchantment == enchantment
    assert weapon.weapon_type == weapon_type
