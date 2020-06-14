class Weapon:
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
                 is_ranged: bool = False):

        Weapon._instance_count += 1

        self.name: str = name
        self._dmg: float = damage
        self.durability_max: int = durability
        self._durability: float = durability
        self.hit_mod: int = hit_modifier
        self.dmg_type: str = damage_type
        self.is_ranged: bool = is_ranged

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: _instance_count
        """
        return Weapon._instance_count

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
            f'is_ranged: {self.is_ranged})'
                )