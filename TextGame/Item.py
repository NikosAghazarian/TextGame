from functools import total_ordering  # For equality operator extrapolation


@total_ordering
class Item:
    """
    A class for generic items.
    """

    def __init__(self, name="default", value: int = 0, weight: float = 0):
        self.name: str = name
        self.value: int = value
        self.weight: float = weight
        self.description: str = 'Default Item'

    @staticmethod
    def gen_health_potion() -> 'Item':
        item: Item = Item('Health Potion', 25, 1)
        item.description = 'A basic healing brew. Heals for 25 HP.'
        return item

    @staticmethod
    def gen_repair_kit() -> 'Item':
        item: Item = Item('Repair Kit', 10, 2)
        item.description = 'A bag filled with oils, cloths, and whetstones. ' \
                           'Repairs 5% of target equipment\'s max durability.'
        return item

    def __str__(self):
        string = f'Name:   {self.name}\n' \
                 f'Value:  {self.value}\n' \
                 f'Weight: {self.weight}\n' \
                 f'Description: {self.description}'
        return string

    def __repr__(self):
        return f'Item({self.name}, {self.value}, {self.weight})'

    def __eq__(self, other):
        return self.name == other

    def __lt__(self, other):
        return self.name < other
