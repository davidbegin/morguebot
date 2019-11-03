import pytest

from lib.morgue_event import MorgueEvent
from lib.event_coordinator import EventCoordinator


@pytest.mark.focus
def test_help_event_coordination():
    morgue_event = MorgueEvent(command="!h?")
    event_coordinator = EventCoordinator(morgue_event)
    assert event_coordinator.lambda_target == "dungeon_gossiper-67e2768"
    result = event_coordinator.coordinate()
    # we want to assert that the dungeon gossiper was called with the aright args
    # or the well tested abstraction was called with the right Args!!!


def test_fetch_event_coordination():
    pass


def test_rune_awards_event_coordination():
    pass


def test_weapon_searching_event_coordination():
    pass
