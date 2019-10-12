from lib.character import Character


def test_find_morgue_file():
    local_mode = True
    character = Character(character="GucciMane", local_mode=local_mode)
    expected_filepath = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/GucciMane.txt"
    assert character.morgue_filepath == expected_filepath


def test_find_morgue_url():
    character = Character(character="GucciMane")
    expected_url = "http://crawl.akrasiac.org/rawdata/GucciMane/GucciMane.txt"
    assert character.morgue_url == expected_url
