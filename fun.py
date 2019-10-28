def hello(name):
    print(f"hello {name}")


class Printer:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"hello {self.name}")

    def goodbye(self):
        print(f"goodbye {self.name}")

    def goodmorning(self):
        print(f"good morning{self.name}")


printer = Printer("ntb899")


printer.hello()
printer.goodbye()
printer.goodmorning()

hello("ntb899")
