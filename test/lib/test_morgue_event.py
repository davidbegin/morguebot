import pytest
from lib.morgue_event import MorgueEvent


def test_event_with_basic_command():
    morgue_event = MorgueEvent(command="!h?")
    assert morgue_event.character is None


def test_event_with_no_character():
    morgue_event = MorgueEvent(command="!fetch", character="beginbot")
    assert morgue_event.character is "beginbot"


def test_event_is_character_command():
    morgue_event = MorgueEvent(command="!fetch", character="beginbot")
    assert morgue_event.is_character_command()
    morgue_event = MorgueEvent(command="!h?")
    assert not morgue_event.is_character_command()


def test_event_is_level_search():
    morgue_event = MorgueEvent(
        command="!spells", character="beginbot", level_barrier="1"
    )
    assert morgue_event.level_barrier
    morgue_event = MorgueEvent(command="!spells", character="beginbot")
    assert not morgue_event.level_barrier


def test_event_with_character():
    pass


def test_event_with_an_arg():
    pass


def test_event_with_2_args():
    pass
