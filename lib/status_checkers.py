from lib.morgue_parser import fetch_altars


# Fun Fact: There are currently 25 gods in DC
def check_for_new_gods(old_altars, morgue_file, printer):
    altars = set(fetch_altars(morgue_file))

    if len(altars) > len(old_altars):
        new_altars = altars.difference(set(old_altars))
        print(f"We Found a new God(s): {new_altars}")
        printer.print_missionary(new_altars)
    else:
        new_altars = {}
    return altars, new_altars
