import pytest

from lib.character import Character


# TODO: Come back and test
def test_compare_morgues():
    character = Character(name="artmatt")
    online_morgue = character.non_saved_morgue_file()
    saved_morgue = character.s3_morgue_file()
    # import pdb
    # pdb.set_trace()
