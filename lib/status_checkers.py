from lib.morgue_parser import fetch_altars


# Fun Fact: There are currently 25 gods in DC
def check_for_new_gods(old_altars, morgue_file, printer):
    altars = set(fetch_altars(morgue_file))

    if old_altars and len(altars) > len(old_altars):
        new_altars = altars.difference(set(old_altars))
        # TODO: make this message work for 1 or more Altars
        print("We Found a new God: {new_altars}")
        printer.print_missionary(new_altars)
    else:
        new_altars = {}
    return altars, new_altars

