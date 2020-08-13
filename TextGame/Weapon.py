import math as math
import random as rand

from TextGame.GameState import GameState
from TextGame.Item import Item


class Weapon(Item):
    """
    Class for weapon items.
    """

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 damage: float = 1,
                 durability: int = 999,
                 hit_modifier: int = 0,
                 damage_type: str = 'Bludgeoning',
                 is_ranged: bool = False,
                 tier: str = 'Common'):

        Weapon._instance_count += 1

        super().__init__(name)

        self._dmg: float = damage
        self.durability_max: int = durability
        self._durability: float = durability
        self.hit_mod: int = hit_modifier
        self.dmg_type: str = damage_type
        self.is_ranged: bool = is_ranged
        self.tier: str = tier

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of Weapon instances alive.

        :return: _instance_count
        """
        return Weapon._instance_count

    @staticmethod
    def create_common_weapon(scaling: int) -> 'Weapon':
        atk: int = int(math.floor(1 + scaling * 0.7))  # Linear.
        dur: int = int(10 + 0.00002 * scaling ** 3)  # Cubic, but very slow start.
        hit_mod: int = int(math.floor(scaling * 0.035))  # Linearly-increasing monotonic step.
        dmg_type: str = GameState.damage_types[rand.randrange(0, 4)]  # Random normal dmg type.
        ranged: bool = True if rand.random() > 0.95 else False  # 5% chance for ranged battle.

        weap: Weapon = Weapon('CommonWeapon', atk, dur, hit_mod, dmg_type, ranged, 'Common')
        weap.value = 100
        weap.weight = 15
        return weap

    @staticmethod
    def create_uncommon_weapon(scaling: int) -> 'Weapon':
        atk: int = int(math.floor(2 + scaling * 0.7))  # Linear.
        dur: int = int(15 + 0.00002 * scaling ** 3)  # Cubic, but very slow start.
        hit_mod: int = int(math.floor(scaling * 0.07))  # Linearly-increasing monotonic step.
        dmg_type: str = GameState.damage_types[rand.randrange(0, 4)]  # Random normal dmg type.
        ranged: bool = True if rand.random() > 0.9 else False  # 10% chance for ranged battle.

        weap: Weapon = Weapon('UncommonWeapon', atk, dur, hit_mod, dmg_type, ranged, 'Uncommon')
        weap.value = 250
        weap.weight = 15
        return weap

    @staticmethod
    def create_rare_weapon(scaling: int) -> 'Weapon':
        atk: int = int(math.floor(3 + scaling * 0.8))  # Linear.
        dur: int = int(30 + 0.00003 * scaling ** 3)  # Cubic, but very slow start.
        hit_mod: int = int(math.floor(scaling * 0.07)) + 1  # Linearly-increasing monotonic step.
        dmg_type: str = GameState.damage_types[rand.randrange(0, len(GameState.damage_types))]  # Random dmg type.
        ranged: bool = True if rand.random() > 0.85 else False  # 15 chance for ranged battle.

        weap: Weapon = Weapon('RareWeapon', atk, dur, hit_mod, dmg_type, ranged, 'Rare')
        weap.value = 500
        weap.weight = 10
        return weap

    @staticmethod
    def create_legendary_weapon(scaling: int) -> 'Weapon':
        atk: int = int(math.floor(5 + scaling * 0.9))  # Linear.
        dur: int = int(100 + 0.00003 * scaling ** 3)  # Cubic, but very slow start.
        hit_mod: int = int(math.floor(scaling * 0.075)) + 4  # Linearly-increasing monotonic step.
        dmg_type: str = GameState.damage_types[rand.randrange(0, len(GameState.damage_types))]  # Random dmg type.
        ranged: bool = True if rand.random() > 0.85 else False  # 15 chance for ranged battle.

        weap: Weapon = Weapon('LegendaryWeapon', atk, dur, hit_mod, dmg_type, ranged, 'Legendary')
        weap.value = 1000
        weap.weight = 20
        return weap

    @staticmethod
    def create_mythic_weapon(scaling: int) -> 'Weapon':
        atk: int = int(math.floor(12 + 0.009 * scaling ** 2))  # Quadratic, out-scales Rare@scaling72, Legend@scaling85.
        dur: int = int(scaling * 0.03 - 2)  # Cubic, but very slow start.
        hit_mod: int = int(math.floor(scaling * 0.1)) + 7  # Linearly-increasing monotonic step.
        dmg_type: str = GameState.damage_types[rand.randrange(0, len(GameState.damage_types))]  # Random dmg type.
        ranged: bool = True if rand.random() > 0.85 else False  # 15 chance for ranged battle.

        weap: Weapon = Weapon('MythicWeapon', atk, dur, hit_mod, dmg_type, ranged, 'Mythic')
        weap.value = 1000
        weap.weight = 5
        return weap

    @staticmethod
    def weapon_gen(scaling: int) -> 'Weapon':
        """
        Generates weapons with random tiers and stats.

        Common-70%, 78% before scaling>40

        Uncommon-15%, 18.5% before scaling>70

        Rare-8% after scaling>40, 10.5% before scaling>100

        Legendary-4.5% after scaling>70

        Mythical-2.5% after scaling>100

        :param scaling: Scaling variable that controls the stat generation. Plus/Minus `0.1*scaling*(random()-0.5)`
        :return: Generated Weapon.
        """

        scaling += scaling * 0.1 * (rand.random()-0.5)
        roll: float = rand.random() * 100

        if roll < 70:  # 70%, 78% before scaling>40
            return Weapon.create_common_weapon(scaling)
        elif roll < 85:  # 15%, 18.5% before scaling>70
            return Weapon.create_uncommon_weapon(scaling)
        elif roll < 93:  # 8% after scaling>40
            if scaling > 40:
                return Weapon.create_rare_weapon(scaling)
            else:
                return Weapon.create_common_weapon(scaling)
        elif roll < 97.5:  # 4.5% after scaling>70
            if scaling > 70:
                return Weapon.create_legendary_weapon(scaling)
            else:
                return Weapon.create_uncommon_weapon(scaling)
        elif roll < 100:  # 2.5% after scaling>100
            if scaling > 100:
                return Weapon.create_mythic_weapon(scaling)
            else:
                return Weapon.create_rare_weapon(scaling)
        else:
            return Weapon.create_common_weapon(scaling)

    @property
    def durability(self) -> float:
        """
        Getter for _durability.

        :return: _durability.
        """
        return self._durability

    @durability.setter
    def durability(self, new_durability: float) -> None:
        """
        Setter for _durability. Contains logic for breakage and negative(invalid) durabilities.
        Also contains logic for excess repair.

        :param new_durability: New value.
        """
        self._durability = new_durability
        if self._durability < 1:
            print(f'{self.name} has broken!')
            self._durability = 0
        elif self._durability > self.durability_max:
            self._durability = self.durability_max
            print(f'{self.name} is fully repaired!')

    @property
    def dmg(self) -> float:
        """
        Getter for _dmg with logic for broken weapons.

        :return: If durability is 0, returns 1, otherwise returns _dmg.
        """

        if self.durability < 1:
            return 1
        return self._dmg

    @dmg.setter
    def dmg(self, new_dmg: float) -> None:
        """
        Setter for _dmg.

        :param new_dmg: Value to set to.
        """

        self._dmg = new_dmg

    def __str__(self):
        x: str = (f'  {self.name}  \n'
                  f'++{"+"*len(self.name)}++\n'
                  f'Tier:         {self.tier}\n'
                  f'Dmg:          {self.dmg}\n'
                  f'Durability:   {self.durability} / {self.durability_max}\n'
                  f'To-Hit Bonus: +{self.hit_mod}\n'
                  f'Dmg Type:     {self.dmg_type}\n'
                  f'Ranged:       {"Yes" if self.is_ranged else "No"}\n'
                  f'++{"+" * len(self.name)}++\n'
                  )
        return x

    def __repr__(self):
        return (
            f'Weapon(name:{self.name}, '
            f'_dmg:{self._dmg}, '
            f'durability_max: {self.durability_max}, '
            f'_durability: {self._durability}, '
            f'hit_mod: {self.hit_mod}, '
            f'dmg_type: {self.dmg_type}, '
            f'is_ranged: {self.is_ranged}, '
            f'tier: {self.tier})'
                )