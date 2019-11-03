import pytest

from lib.morgue_event_router import MorgueEventRouter


def test_morgue_event_router_is_real():
    assert MorgueEventRouter()
