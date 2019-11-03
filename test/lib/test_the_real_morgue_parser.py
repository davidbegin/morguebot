import pytest

from lib.the_real_morgue_parser import MorgueParser


def test_morgue_parser_is_real_i_swear():
    morgue_file = open("support/kilrfish.txt").read()
    morgue_parser = MorgueParser(morgue_file)
    assert True


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


@pytest.mark.focus
def test_fetch_armour():
    character_name = "kaostheory"
    morgue_parser = MorgueParser(open(f"support/{character_name}.txt").read())
    expected_armour = ""
    armour = morgue_parser.armour()

    # morgue_file = open(morgue_file_path).read()
    # import pdb; pdb.set_trace()
