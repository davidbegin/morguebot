from lib.morgue_finder import find_morgue_file


def test_find_morgue_file():
    assert 1 == 2
    character = "GucciMane"
    local_mode = True

    assert (
        find_morgue_file(character=character, local_mode=local_mode)
        == "{Morgue_Home}/GucciMane.txt"
    )
    # def find_morgue_file(
    #     character=None, local_mode=None, morgue_file_path=None, morgue_url=None
    # ):
    # pass
