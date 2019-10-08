from lib.morgue_finder import find_morgue_filepath


def test_find_morgue_file():
    character = "GucciMane"
    local_mode = True
    expected_filepath = f"/Users/begin/Library/Application Support/Dungeon Crawl Stone Soup/morgue/GucciMane.txt"
    result = find_morgue_filepath(character=character, local_mode=local_mode)
    assert result == expected_filepath

    # def find_morgue_file(
    #     character=None, local_mode=None, morgue_file_path=None, morgue_url=None
    # ):
    # pass
