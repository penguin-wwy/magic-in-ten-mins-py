def get_level_with_match(s: int) -> str:
    assert s in range(0, 101)
    match s:
        case num if num >= 90: return 'A'
        case num if num >= 90: return 'B'
        case num if num >= 90: return 'C'
        case num if num >= 90: return 'D'
        case _: return 'E'


SCORE = [90, 80, 70, 60]
LEVEL = ['A', 'B', 'C', 'D', 'E']


def get_level_with_loop(s: int) -> str:
    pos = 0
    while pos < len(SCORE) and s < SCORE[pos]:
        pos += 1
    return LEVEL[pos]


class Item:

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        self.count: int = 0


class ShopList:

    ITEMS = [
        Item("water", 1),
        Item("cola", 2),
        Item("choco", 5),
    ]

    def buy(self, name: str) -> 'ShopList':
        for x in filter(lambda i: i.name == name, ShopList.ITEMS):
            x.count += 1
        return self


class SimpleUI:

    shop = ShopList()

    events = {
        0: lambda: SimpleUI.shop.buy("water"),
        1: lambda: SimpleUI.shop.buy("cola"),
        2: lambda: print(SimpleUI.shop),
        3: lambda: exit(0),
    }

    def run_event(self, e: int):
        self.events[e]()


class ComplexUI:

    x: int = 0
    y: int = 0

    def w(self):
        self.y += 1

    def s(self):
        self.y -= 1

    def a(self):
        self.x -= 1

    def d(self):
        self.x += 1

    MOVE_EVENTS = {
        'w': lambda s: s.w(),
        'a': lambda s: s.a(),
        's': lambda s: s.s(),
        'd': lambda s: s.d(),
        'e': lambda s: print(s),
        'q': lambda s: s.draw_menu()
    }

    def move(self, c: str):
        assert c in ComplexUI.MOVE_EVENTS
        ComplexUI.MOVE_EVENTS[c](self)

    def draw_move(self):
        """ draw move """

    MENU_EVENTS = {
        'p': lambda s: s.draw_move(),
        'q': lambda s: s.exit(),
    }

    def menu(self, c: str):
        assert c in ComplexUI.MENU_EVENTS
        ComplexUI.MENU_EVENTS[c](self)

    def draw_menu(self):
        """ draw menu """

    def exit(self):
        """ exit """
