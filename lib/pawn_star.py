
UNRANDS = [
    # Rings??
    # "ring of the Mage {Wiz MR++ Int+3}",

    # This aint Right
    "+14 obsidian axe {chop, +Fly SInv *Curse}",

    # This is right
    "the cursed +14 obsidian axe {chop, +Fly SInv *Curse}",
    "the +12 Vampire's Tooth {vamp}",
    # "sword" ,
    "autumn katana" ,
    "storm bow" ,
    "lance" ,
    "maxwell's thermic engine" ,
    "wrath of trog" ,
    "heavy crossbow" ,
    "mithril axe" ,
    "arc blade" ,
    "dark maul" ,
    "majin-bo" ,
    "captain's cutlass" ,
    "spriggan's knife" ,
    "obsidian axe" ,
]




class PawnStar():
    def __init__(self, weapon):
        self.weapon = weapon

    def is_unrand(self):
        return len([ unrand for unrand in UNRANDS if unrand in self.weapon ]) > 0


