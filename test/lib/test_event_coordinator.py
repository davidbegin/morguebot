import pytest
from pytest_mock import mocker

from lib.morgue_event import MorgueEvent
from lib.event_coordinator import EventCoordinator


@pytest.mark.focus
def test_help_event_coordination(mocker):
    morgue_event = MorgueEvent(command="!h?")
    event_coordinator = EventCoordinator(morgue_event)
    mocker.patch.object(event_coordinator, "invoke_lambda")
    event_coordinator.invoke_lambda.return_value = "I was invoked!!"
    assert event_coordinator.lambda_target == "dungeon_gossiper-67e2768"
    result = event_coordinator.coordinate()
    assert result == "I was invoked!!"


def test_fetch_event_coordination():
    pass


def test_rune_awards_event_coordination():
    pass


def test_weapon_searching_event_coordination():
    pass
