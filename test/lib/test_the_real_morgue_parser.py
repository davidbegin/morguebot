import pytest

from lib.the_real_morgue_parser import MorgueParser


def test_parse_spells():
    morgue_file = open("support/kilrfish.txt").read()
    morgue_parser = MorgueParser(morgue_file)
    spells = morgue_parser.spells()
    expected_spells = [
        "Animate Skeleton         Necr           N/A          98%         1    ##.....",
        "Apportation              Tloc           #.....       98%         1    ##.....",
        "Confusing Touch          Hex            #.....       98%         1    ##.....",
        "Corona                   Hex            #......      98%         1    ##.....",
        "Infusion                 Chrm           #...         98%         1    ##.....",
        "Shock                    Conj/Air       #...         98%         1    ##.....",
        "Summon Small Mammal      Summ           #...         98%         1    ##.....",
        "Call Imp                 Summ           #.......     99%         2    ###....",
        "Ensorcelled Hibernation  Hex/Ice        #.....       99%         2    ###....",
        "Shroud of Golubria       Chrm/Tloc      #.....       99%         2    ###....",
        "Song of Slaying          Chrm           #.......     99%         2    ###....",
        "Swiftness                Chrm/Air       #.......     99%         2    ###....",
        "Call Canine Familiar     Summ           #.......     100%        3    ####...",
        "Confuse                  Hex            #.......     100%        3    ####...",
        "Dazzling Spray           Conj/Hex       #.....       100%        3    ####...",
        "Portal Projectile        Hex/Tloc       #.....       100%        3    ####...",
        "Regeneration             Chrm/Necr      #.........   100%        3    ####...",
        "Spectral Weapon          Hex/Chrm       #.......     100%        3    ####...",
        "Static Discharge         Conj/Air       #.......     100%        3    ####...",
        "Summon Guardian Golem    Hex/Summ       #.......     100%        3    ####...",
        "Tukima's Dance           Hex            #.......     100%        3    ####...",
        "Airstrike                Air            #.........   100%        4    #####..",
        "Ice Form                 Ice/Tmut       #.......     100%        4    #####..",
        "Leda's Liquefaction      Hex/Erth       #.........   100%        4    #####..",
        "Summon Ice Beast         Ice/Summ       #.......     100%        4    #####..",
        "Summon Lightning Spire   Summ/Air       #.......     100%        4    #####..",
        "Lightning Bolt           Conj/Air       #.........   100%        5    ######.",
        "Metabolic Englaciation   Hex/Ice        #.........   100%        5    ######.",
        "Bolt of Cold             Conj/Ice       #.........   100%        6    #######",
        "Freezing Cloud           Conj/Ice/Air   #.........   100%        6    #######",
        "Ozocubu's Refrigeration  Ice            #.........   100%        6    #######",
        "Simulacrum               Ice/Necr       #.........   100%        6    #######",
    ]

    assert spells == expected_spells


def test_overview():
    morgue_file = open("support/Fa.txt").read()
    morgue_parser = MorgueParser(morgue_file)
    overview = morgue_parser.overview()
    expected_overview = "Fa the Merry Centaur (Centaur Hunter)  XL:      27  Health:  243/243      Location: Pandemonium."
    assert overview == expected_overview


@pytest.mark.parametrize(
    "character_name,expected_runes",
    [
        (
            "artmatt",
            "decaying, serpentine, slimy, silver, golden, iron, obsidian,\nicy, bone, abyssal, demonic, glowing, fiery",
        ),
        ("sunspire", "serpentine, barnacled, silver"),
        ("GucciMane", None),
    ],
)
def test_runes(character_name, expected_runes):
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    runes = morgue_parser.runes()
    assert runes == expected_runes


def test_fetch_armour():
    character_name = "kaostheory"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected_armour = [" g - a +0 pair of boots (worn)", " h - a +0 ring mail (worn)"]
    armour = morgue_parser.armour()
    assert armour == expected_armour


def test_mutations():
    character_name = "kilrfish"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = "retaliatory headbutt, horns 2"
    result = morgue_parser.mutations()
    assert result == expected


def test_jewellery():
    character_name = "kilrfish"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [
        "an uncursed ring of resist corrosion",
        "a +3 ring of strength (left hand)",
        "a ring of poison resistance (right hand)",
        "an amulet of regeneration (around neck)",
        "an uncursed ring of fire",
        "an uncursed ring of flight",
    ]
    result = morgue_parser.jewellery()
    assert result == expected


def test_scrolls():
    character_name = "GucciMane"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [" b - a scroll labeled BUCEUFOSTE"]
    result = morgue_parser.scrolls()
    assert result == expected


def test_potions():
    character_name = "sunspire"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [
        " q - 23 potions of mutation",
        " r - 14 potions of curing",
        " t - a potion of cancellation",
        " v - a potion of magic",
        " z - 5 potions of brilliance",
        " D - 5 potions of resistance",
        " J - a potion of berserk rage",
        " S - 5 potions of haste",
        " Z - 7 potions of flight",
    ]
    result = morgue_parser.potions()
    assert result == expected


def test_weapons():
    character_name = "sunspire"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [
        "a +9 scimitar of holy wrath (weapon)",
        "the +8 arc blade {discharge, rElec}",
        "a +7 whip of pain",
        "a +5 scimitar of pain",
    ]
    result = morgue_parser.weapons()
    assert result == expected


def test_skills():
    character_name = "sunspire"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [
        " + Level 17.1 Fighting",
        " + Level 16.6 Short Blades",
        " + Level 17.1 Long Blades",
        " + Level 16.6 Axes",
        " + Level 16.6 Maces & Flails",
        " + Level 16.6 Polearms",
        " + Level 16.6 Staves",
        " + Level 16.6 Slings",
        " + Level 16.6 Bows",
        " + Level 16.6 Crossbows",
        " + Level 16.8 Throwing",
        " + Level 16.8 Armour",
        " + Level 17.1 Dodging",
        " + Level 16.6 Stealth",
        " + Level 16.6 Shields",
        " + Level 16.6 Unarmed Combat",
        " + Level 17.2 Spellcasting",
        " + Level 14.3 Conjurations",
        " + Level 14.3 Hexes",
        " + Level 14.3 Charms",
        " + Level 14.3 Summonings",
        " + Level 14.3 Necromancy",
        " + Level 15.1 Translocations",
        " + Level 14.3 Transmutations",
        " + Level 14.3 Fire Magic",
        " + Level 14.3 Ice Magic",
        " + Level 14.3 Air Magic",
        " + Level 14.3 Earth Magic",
        " + Level 14.3 Poison Magic",
        " + Level 17.9 Invocations",
        " + Level 16.6 Evocations",
    ]
    result = morgue_parser.skills()
    assert result == expected


def test_gods():
    character_name = "sunspire"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected = [
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
        "Zin",
        "The Shining One",
        "Beogh",
    ]
    result = morgue_parser.gods()
    assert result == expected
