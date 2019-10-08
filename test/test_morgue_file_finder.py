from lib.morgue_finder import _find_morgue_filepath
from lib.morgue_finder import _find_morgue_url


def test_find_morgue_file():
    character = "GucciMane"
    local_mode = True

    expected_filepath = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/GucciMane.txt"
    result = _find_morgue_filepath(character=character)
    assert result == expected_filepath


def test_find_morgue_url():
    character = "GucciMane"
    expected_url = "http://crawl.akrasiac.org/rawdata/GucciMane/GucciMane.txt"
    result = _find_morgue_url(character=character)
    assert result == expected_url
