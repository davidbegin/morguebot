import pytest

from lib.skill import Skill
from lib.skill_factory import SkillFactory


def test_skill_factory_is_a_good_clean_factory():
    raw_skill = "+ Level 26.9 Maces & Flails"
    subject = SkillFactory(raw_skill).new()
    assert subject.level == 26.9
    assert subject.skill_type == "Maces & Flails"
    assert subject.status == "+"
