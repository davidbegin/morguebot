from lib.character import Character


def test_morgue_filepath():
    local_mode = True
    character = Character(name="GucciMane", local_mode=local_mode)
    expected_filepath = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/GucciMane.txt"
    assert character.morgue_filepath == expected_filepath


def test_morgue_url():
    character = Character(name="GucciMane")
    expected_url = "http://crawl.akrasiac.org/rawdata/GucciMane/GucciMane.txt"
    assert character.morgue_url == expected_url
