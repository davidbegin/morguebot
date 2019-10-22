import pytest

from lib.item_parser import parse_weapon


# "a +9 dagger of speed"
# "a +3 antimagic broad axe"
# @pytest.mark.parametrize(
#     "weapon,expected",
#     [
#         (
#             "the +9 sword of Zonguldrok (weapon) {reap}",
#             {"name": "long sword", "modifier": 9},
#         ),
#         ("the -5 short sword of Begin {slay}", {"name": "short sword", "modifier": -5}),
#         # "+4 Makhleb's Approval (weapon) {speed, MP+9 Str+4 Dex-3}", {}
#     ],
# )
def test_parse_weapon():
    # 'the +8 storm bow {elec, penet}'
    # the +8 morningstar "Aho Hol" (weapon) {flame, rC++}
    weapon_input = "a +7 blowgun"
    result = parse_weapon(weapon_input)
    expected = {"name": "blowgun", "modifier": 7, "type": "Throwing"}
    assert result == expected
