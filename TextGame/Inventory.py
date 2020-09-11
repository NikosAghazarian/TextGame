class Inventory:

    def __init__(self):  # Unlimited capacity
        self.stored_items: list = []
        self.max_weight: int = 20  # Unused
        self.weight: float = 0  # Unused
        self.max_items: int = 4  # Unused
        self._gold: int = 0

    @property
    def gold(self) -> int:
        return self._gold

    @gold.setter
    def gold(self, new_value: int) -> None:
        if new_value < 0:
            raise ValueError('Gold cannot be negative.')
        else:
            self._gold = new_value

    def store(self, item: 'Item') -> None:
        self.stored_items.append(item)

    def remove_item(self, item_name: str) -> None:  # fix this
        if item_name not in self:
            print(f'{item_name} not found.')
        else:
            self.stored_items.remove(item_name)

    def __str__(self):
        string = f'Gold: {self.gold}\n-----------\n'
        for item in self:
            string += f'{item}\n-----------\n'
        return string

    def __contains__(self, item_name):
        return True if item_name in self.stored_items else False

    def __iter__(self):
        return iter(self.stored_items)

    def __len__(self):
        return len(self.stored_items)
