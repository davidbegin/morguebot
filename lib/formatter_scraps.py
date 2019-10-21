# from lib.morgue_parser import fetch_resistance
# from lib.morgue_parser import fetch_trait
# from lib.morgue_parser import fetch_mr
# from lib.morgue_parser import fetch_stealth
#         # elif command == "!stlth":
#         #     self.print_stealth()
#         # elif command == "!mr":
#         #     return self.print_mr()
#         # elif command == "!maxR":
#         #     return self.print_max_resistance()
#         # elif command == "!gods":
#         #     return self.print_gods()
#         # elif command == "!mf":
#         #     pass
#         # elif command in RESISTANCES:
#         #     return self.print_resistance(command[1:])
#         # elif command in TRAITS:
#         #     return self.print_traits(command)

#     def print_missionary(self, new_altars):
#         return ["MercyWing1 New Gods! MercyWing2", ", ".join(new_altars)]

#     # ========================================================================================

#     # def print_traits(self, trait_type, morgue_file):
#     #     trait = fetch_trait(morgue_file, trait_type[1:])

#     #     if trait:
#     #         trait_str = f"{trait_type[1:]}:   {trait}"
#     #         print("\n\033[35m" + trait_str + "\033[0m")
#     #         return trait_str
#     #     else:
#     #         print("\n\033[35m" + "No TRAIT FOUND! " + "\033[0m")

#     # def print_resistance(self, resistance_type, morgue_file):
#     #     if ALIASES.get(resistance_type, None):
#     #         resistance = fetch_resistance(morgue_file, ALIASES[resistance_type])
#     #     else:
#     #         resistance = fetch_resistance(morgue_file, resistance_type)

#     #     if resistance:
#     #         resistance_str = f"{resistance_type}:   {resistance}"
#     #         print("\n\033[35m" + resistance_str + "\033[0m")
#     #         return resistance_str
#     #     else:
#     #         print("\n\033[35m" + "No Resistance FOUND! " + "\033[0m")

#     def print_mr(self, morgue_file):
#         return self.print_command("Magic Resistance", fetch_mr(morgue_file))

#     def print_stealth(self, morgue_file):
#         return self.print_command("Stealth", fetch_stealth(morgue_file))


# # ========================================================================================

# # I Need a better data struct for aliases
# ALIASES = {"rF": "rFire", "rE": "rElec", "rC": "rCold", "rP": "rPois", "MR": "TODO"}

# RESISTANCES = ["!rF", "!rFire", "!rCold", "!rNeg", "!rPois", "!rE", "!rElec", "!rCorr"]
# TRAITS = ["!SeeInvis", "!Gourm", "!Faith", "!Spirit", "!Reflect", "!Harm"]

# COMMANDS_WITH_NO_ARGS = (
#     [
#         "!overview",
#         "!mr",
#         "!stlth",
#         "!mutations",
#         "!jewellery",
#         "!scrolls",
#         "!potions",
#         "!weapons",
#         "!armour",
#         "!skills",
#         "!spells",
#         "!h?",
#         "!maxR",
#         "!mf",
#         "!gods",
#     ]
#     + RESISTANCES
#     + TRAITS
# )
