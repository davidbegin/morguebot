import pytest

from lib.morgue_event_router import MorgueEventRouter
from lib.morgue_event import MorgueEvent


def test_help_event():
    morgue_event = MorgueEvent(command="!h?")
    dest_lambda = MorgueEventRouter(morgue_event).dest_lambda()
    assert dest_lambda == "dungeon_gossiper"


def test_fetch_event():
    morgue_event = MorgueEvent(command="!fetch", character="beginbot")
    dest_lambda = MorgueEventRouter(morgue_event).dest_lambda()
    assert dest_lambda == "morgue_stalker"


def test_rune_awards_event():
    morgue_event = MorgueEvent(command="!rune_awards")
    dest_lambda = MorgueEventRouter(morgue_event).dest_lambda()
    assert dest_lambda == "dungeon_gossiper"
