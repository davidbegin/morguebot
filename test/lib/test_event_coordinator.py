import pytest

from lib.event_coordinator import EventCoordinator


def test_event_coordinator_is_real():
    assert EventCoordinator()
