class Inventory:

    def __init__(self):
        self.storedItems: list = []
        self.max_weight: int = 20
        self.weight: float = 0
        self.max_items: int = 4
        self._gold: int = 0

    @property
    def gold(self) -> int:
        return self._gold

    @gold.setter
    def gold(self, new_value: int):
        if new_value < 0:
            raise ValueError('Gold cannot be negative.')
        else:
            self._gold = new_value

    def store(self, item) -> None:
        self.storedItems.append(item)

    def retrieve(self, item_name) -> None:
        try:
            item = next(x for x in self.storedItems if x == item_name)  # Gets first match from inventory
        except StopIteration:
            print('Item not found.')
        else:
            return item
