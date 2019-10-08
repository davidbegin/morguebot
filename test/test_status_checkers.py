from lib.status_checkers import check_for_new_gods
from support.fake_printer import FakePrinter

def test_check_for_new_gods():
    current_altars = {
        "Ashenzari",
        "Cheibriados",
        "Dithmenos",
        "Elyvilon",
        "Fedhas",
        "Gozag",
        "Hepliaklqana",
        "Kikubaaqudgha",
        "Makhleb",
        "Nemelex Xobeh",
        "Okawaru",
        "Qazlal",
        "Ru",
        "Sif Muna",
        "Trog",
        "Uskayaw",
        "Vehumet",
        "Wu Jian",
        "Xom",
        "Yredelemnul",
        "The Shining One",
    }
    old_altars = {"Xom"}
    morgue_file = open("Support/WilliamGates.txt").read()
    all_altars, new_altars = check_for_new_gods(old_altars, morgue_file, FakePrinter())
    # import code; code.interact(local=dict(globals(), **locals()))
    assert set(new_altars) == current_altars.difference(old_altars)

