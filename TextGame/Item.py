class Item:
    """
    A class for generic items.
    """

    def __init__(self, name="default", value: int = 0, weight: float = 0):
        self.name: str = name
        self.value: int = value
        self.weight: float = weight
        self.description: str = 'Default Item'
