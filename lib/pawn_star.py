UNRANDS = [
    # Rings??
    # "ring of the Mage {Wiz MR++ Int+3}",
    # This aint Right
    "+14 obsidian axe {chop, +Fly SInv *Curse}",
    # This is right
    "the cursed +14 obsidian axe {chop, +Fly SInv *Curse}",
    "the +12 Vampire's Tooth {vamp}",
    # "sword" ,
    "autumn katana",
    "storm bow",
    "lance",
    "maxwell's thermic engine",
    "wrath of trog",
    "heavy crossbow",
    "mithril axe",
    "arc blade",
    "dark maul",
    "majin-bo",
    "captain's cutlass",
    "spriggan's knife",
    "obsidian axe",
    "vampire's tooth",
    'dagger "morg"',
    "spriggan's knife" "arc blade",
    "captain's cutlass",
    "quick blades 'gyre' and 'gimble'",
    "singing sword",
    "sword of zonguldrok",
    "maxwell's thermic engine",
    "autumn katana",
    "demon blade 'bloodbane'",
    "demon blade 'leech'",
    "zealot's sword",
    "sword of cerebov",
    "plutonium sword",
    "staff of dispater",
    "sceptre of asmodeus",
    "staff of olgreb",
    "elemental staff",
    "staff of wucad mu",
    "majin-bo",
    "lajatang of order",
    "mithril axe 'arga'",
    "obsidian axe",
    "wrath of trog",
    "frozen axe 'frostbite'",
    "axe of woe",
    "lance 'wyrmbane'",
    "trident of the octopus king",
    "demon trident 'rift'",
    "glaive of the guard",
    "glaive of prune",
    "scythe of curses",
    "scythe 'finisher'",
    "shillelagh 'devastator'",
    "whip 'snakebite'",
    "morningstar 'eos'",
    "demon whip 'spellbinder'",
    "sceptre of torment",
    "great mace 'firestarter'",
    "mace of variability",
    "giant club 'skullcrusher'",
    "dark maul",
    "fustibalus 'punk'",
    "longbow 'zephyr'",
    "storm bow",
    "longbow 'piercer'",
    "arbalest 'damnation'",
    "heavy crossbow 'sniper'",
]


class PawnStar:
    def __init__(self, weapon):
        self.weapon = weapon

    def is_unrand(self):
        return (
            len([unrand for unrand in UNRANDS if unrand.lower() in self.weapon.lower()])
            > 0
        )
