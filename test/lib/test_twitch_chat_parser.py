import pytest

from lib.twitch_chat_parser import TwitchChatParser


@pytest.mark.focus
def test_help_command():
    event_morgue = TwitchChatParser("!h?").parse()
    assert event_morgue.command == "!h?"


@pytest.mark.focus
def test_fetch_command():
    event_morgue = TwitchChatParser("!fetch beginbot").parse()
    assert event_morgue.command == "!fetch"
    assert event_morgue.character == "beginbot"


def test_searching_weapons():
    pass


def test_rune_awards():
    pass
