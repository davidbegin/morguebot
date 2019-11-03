import pytest

from lib.command_line_parser import CommandLineParser


def test_command_line_parser_is_real():
    assert CommandLineParser()
