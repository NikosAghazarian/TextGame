from TextGame.GameState import GameState


class Armor:
    """
    Armor item class.
    """

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 durability: int = 999,
                 resistances=None,
                 defense: int = 0,
                 armor_class: int = 0):

        if resistances is None:
            resistances = []

        Armor._instance_count += 1

        self.name: str = name
        self.durability_max: int = durability
        self._durability: float = durability
        self._resistances: list = resistances
        self._defense: int = defense
        self.AC: int = armor_class  # Armor Class

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, new_durability: float):
        self._durability = new_durability
        if self._durability < 1:
            print(f'{self.name} has broken!')
            self._durability = 0
        elif self._durability > self.durability_max:
            self._durability = self.durability_max
            print(f'{self.name} is fully repaired!')

    @property
    def defense(self):
        if self.durability < 1:
            return 0
        return self._defense

    @defense.setter
    def defense(self, new_defense: float):
        self._defense = new_defense

    @property
    def resistances(self):
        if self.durability < 1:
            return []
        return self._resistances

    @resistances.setter
    def resistances(self, new_resistances: list):
        self._resistances = new_resistances

    def add_resistance(self, new_resistance: str):
        if new_resistance in GameState.damage_types:
            self._resistances.append(new_resistance)
        else:
            raise ValueError('Not a valid resistance.')

    def __str__(self):
        x: str = (f'  {self.name}  \n'
                  f'++{"+"*len(self.name)}++\n'
                  f'Durability:  {self.durability} / {self.durability_max}\n'
                  f'Resistances: {", ".join(self.resistances)}\n'
                  f'Defense:     {self.defense}\n'
                  f'AC:          {self.AC}\n'
                  f'++{"+" * len(self.name)}++\n')
        return x

    def __repr__(self) -> str:
        return (
            f'Armor(name:{self.name}, '
            f'durability_max:{self.durability_max}, '
            f'_durability:{self._durability}, '
            f'_resistances:{self._resistances}, '
            f'_defense:{self._defense}, '
            f'AC:{self.AC})'
        )
