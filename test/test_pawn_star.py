import pytest

from lib.pawn_star import PawnStar


@pytest.mark.focus
def test_is_unrand():
    weapon = ("the cursed +14 obsidian axe {chop, +Fly SInv *Curse}",)
    subject = PawnStar(weapon)
    assert subject.is_unrand()
