import pytest

from lib.twitch_chat_parser import TwitchChatParser


def test_help_command():
    morgue_event = TwitchChatParser("!h?").parse()
    assert morgue_event.command == "!h?"


def test_fetch_command():
    morgue_event = TwitchChatParser("!fetch beginbot").parse()
    assert morgue_event.command == "!fetch"
    assert morgue_event.character == "beginbot"
    assert morgue_event.args == []


def test_searching_weapons():
    morgue_event = TwitchChatParser("!weapons beginbot axe").parse()
    assert morgue_event.command == "!weapons"
    assert morgue_event.character == "beginbot"
    assert morgue_event.args == ["axe"]


def test_rune_awards():
    morgue_event = TwitchChatParser("!rune_awards").parse()
    assert morgue_event.command == "!rune_awards"
    assert morgue_event.character == None
    assert morgue_event.args == []
