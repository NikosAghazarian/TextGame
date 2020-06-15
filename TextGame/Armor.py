import math as math
import random as rand

from TextGame.GameState import GameState


class Armor:
    """
    Armor item class.
    """

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 durability: int = 99999,
                 resistances=None,
                 defense: int = 0,
                 armor_class: int = 0,
                 tier: str = 'Common'):

        if resistances is None:
            resistances = []

        Armor._instance_count += 1

        self.name: str = name
        self.durability_max: int = durability
        self._durability: float = durability
        self._resistances: list = resistances
        self._defense: int = defense
        self.AC: int = armor_class  # Armor Class
        self.tier: str = tier

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of Weapon instances alive.

        :return: _instance_count
        """
        return Armor._instance_count

    @staticmethod
    def create_common_armor(scaling: int):
        dur: int = int(30 + 0.00002 * scaling ** 3)  # Cubic, but very slow start.
        res: str = None
        defense: int = int(math.ceil(0.6 * pow(math.log10(1 + scaling**2), 2.45)))
        ac: int = int(math.floor(scaling * 0.08))
        return Armor('CommonArmor', dur, res, defense, ac, 'Common')

    @staticmethod
    def create_uncommon_armor(scaling: int):
        dur: int = int(35 + 0.00002 * scaling ** 3)  # Cubic, but very slow start.
        res: str = None
        defense: int = int(math.ceil(0.7 * pow(math.log10(1 + scaling ** 2), 2.45)))
        ac: int = int(math.floor(scaling * 0.1)) + 1
        return Armor('UncommonArmor', dur, res, defense, ac, 'Uncommon')

    @staticmethod
    def create_rare_armor(scaling: int):
        dur: int = int(50 + 0.00003 * scaling ** 3)  # Cubic, but very slow start.
        res: str = GameState.damage_types[rand.randrange(0, 4)]  # Picks a random normal resistance
        defense: int = int(math.ceil(0.8 * pow(math.log10(1 + scaling ** 2), 2.45)))
        ac: int = int(math.floor(scaling * 0.1)) + 2
        return Armor('RareArmor', dur, res, defense, ac, 'Rare')

    @staticmethod
    def create_legendary_armor(scaling: int):
        dur: int = int(200 + 0.00003 * scaling ** 3)  # Cubic, but very slow start.
        res: str = rand.sample(GameState.damage_types, range(1, 4))  # Picks 1-3 random resistances
        defense: int = int(math.ceil(0.9 * pow(math.log10(1 + scaling ** 2), 2.45)))
        ac: int = int(math.floor(scaling * 0.1)) + 3
        return Armor('LegendaryArmor', dur, res, defense, ac, 'Legendary')

    @staticmethod
    def create_mythic_armor(scaling: int):
        dur: int = int(2 + 0.0003 * scaling ** 2)  # Quadratic, but very slow start.
        res: str = rand.sample(GameState.damage_types, range(1, 4))  # Picks 1-3 random resistances
        defense: int = int(math.ceil(0.6 * pow(math.log10(1 + scaling ** 2), 2.35)))
        ac: int = int(math.floor(scaling * 0.1)) + 9
        return Armor('MythicArmor', dur, res, defense, ac, 'Mythic')

    @staticmethod
    def armor_gen(scaling: int) -> 'Armor':
        """
        Generates armor with random tiers and stats.

        Common-70%, 78% before scaling>40

        Uncommon-15%, 18.5% before scaling>70

        Rare-8% after scaling>40, 10.5% before scaling>100

        Legendary-4.5% after scaling>70

        Mythical-2.5% after scaling>100

        :param scaling: Scaling variable that controls the stat generation. Plus/Minus `0.1*scaling*(random()-0.5)`
        :return: Generated Armor.
        """

        scaling += int(scaling * 0.1 * (rand.random() - 0.5))
        roll: float = rand.random() * 100

        if roll < 70:  # 70%, 78% before scaling>40
            return Armor.create_common_armor(scaling)
        elif roll < 85:  # 15%, 18.5% before scaling>70
            return Armor.create_uncommon_armor(scaling)
        elif roll < 93:  # 8% after scaling>40
            if scaling > 40:
                return Armor.create_rare_armor(scaling)
            else:
                return Armor.create_common_armor(scaling)
        elif roll < 97.5:  # 4.5% after scaling>70
            if scaling > 70:
                return Armor.create_legendary_armor(scaling)
            else:
                return Armor.create_uncommon_armor(scaling)
        elif roll < 100:  # 2.5% after scaling>100
            if scaling > 100:
                return Armor.create_mythic_armor(scaling)
            else:
                return Armor.create_rare_armor(scaling)
        else:
            return Armor.create_common_armor(scaling)

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
