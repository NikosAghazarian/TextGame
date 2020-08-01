import random as rand

from TextGame.GameState import GameState
from TextGame.Inventory import Inventory
from TextGame.ActorUnit import ActorUnit
from TextGame.Armor import Armor
from TextGame.Weapon import Weapon
from TextGame.Menu import Menu


class Player(ActorUnit):
    """
    The player unit, extends ActorUnit.
    """

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5)
                 ):

        super().__init__(name, health, starter_weapon, starter_armor)
        self._xp: int = 0
        self.next_level_xp_threshold: int = 1
        self._lvl: int = 1

    def turn(self) -> None:
        Menu.menu_logic()

    def target_selector(self) -> 'ActorUnit':
        banned_index = Menu.targeting()
        chosen_index: int = -1
        max_index: int = len(GameState.actors)-1
        while chosen_index <= 0 or max_index < chosen_index or chosen_index in banned_index:
            try:
                chosen_index = int(input('Choose a valid target ID: '))
            except ValueError:
                print('Not a valid numeric ID.')
        return GameState.actors[chosen_index]

    def weapon_selector(self) -> Weapon:
        chosen_index: int = -1

        Menu.player_weapons()
        max_index: int = len(self.weapons)-1
        while chosen_index < 0 or chosen_index > max_index:
            try:
                chosen_index = int(input('Choose a valid weapon ID: '))
            except ValueError:
                print('Not a valid numeric ID.')

        return self.weapons[chosen_index]

    def armor_selector(self) -> Armor:
        """
        Helper function to allow display and selection of armor from inventory.

        :return: Armor
        """

        armors: list = [GameState.player_actor.armor]
        armors.extend([item for item in GameState.player_actor.inventory.storedItems if type(item) == 'Armor'])
        Menu.player_armors(armors)
        chosen_index: int = -1
        max_index: int = len(armors)-1

        while chosen_index < 0 or chosen_index > max_index:
            try:
                chosen_index = int(input('Choose a valid armor ID: '))
            except ValueError:
                print('Not a valid numeric ID.')

        return armors[chosen_index]

    def don_armor(self) -> None:
        """
        Allows swapping of equipped armor with armor in the inventory.

        :return: None
        """

        new_armor: Armor = self.armor_selector()
        if new_armor.durability >= 1:  # Check if broken.
            self.inventory.store(self.armor)  # Store current armor.
            self.inventory.retrieve(new_armor)  # Take out new armor.
            self.armor = new_armor  # Equip.
        else:
            print('This armor is too damaged to use.')

    def heal(self) -> None:
        """
        Heal action of player.

        :return: None
        """

        self.health += 3

    def repair(self) -> None:
        """
        Repair player equipment.

        :return: None
        """

        command = ''
        while command not in ['a', 'armor', 'w', 'weapon']:
            command = input('Repair (A)rmor or (W)eapon: ').lower()

        if command in ['a', 'armor']:
            item: Armor = self.armor_selector()
            item.durability += item.durability_max * 0.05
        elif command in ['w', 'weapon']:
            item: Weapon = self.weapon_selector()
            self.modify_weapon_durability(item, item.durability_max * 0.05)
        else:
            raise ValueError('Not sure how you got here.')
        print(f'{item.name}: {item.durability} / {item.durability_max}')

    def shop(self) -> None:

        Menu.shop()

    @property
    def xp(self) -> int:
        """
        TODO: Bug - setter is broken; stops at lvl 3, 0/4 xp

        :return:
        """
        return self._xp

    @xp.setter
    def xp(self, new_xp: int) -> None:
        if new_xp >= self.next_level_xp_threshold:
            self.lvl += 1
            remaining_xp = new_xp - self.next_level_xp_threshold + self.xp
            self.xp = 0
            self.next_level_xp_threshold += self.next_level_xp_threshold
            self.xp += remaining_xp
        else:
            _xp = new_xp

    @property
    def lvl(self) -> int:
        return self._lvl

    @lvl.setter
    def lvl(self, new_lvl: int) -> None:
        print("Level Up!")
        self._lvl = new_lvl

    def __str__(self) -> str:
        character_stat: str = (
            f'Name:    {self.name}\n'
            f'HP:      {self.health} / {self.health_max}\n'
            f'Level:   {self._lvl}\n'
            f'EXP:     {self.xp} / {self.next_level_xp_threshold}\n'
            f'=====================================\n'
            f'Weapons\n'
            f'=====================================\n'
        )
        weapon_stat: str = ""
        for weapon in self.weapons:
            weapon_stat += str(weapon)
        armor_header: str = (
            f'=====================================\n'
            f'Armor\n'
            f'=====================================\n'
        )
        armor_stat: str = str(self.armor)
        return character_stat + weapon_stat + armor_header + armor_stat

    def __repr__(self) -> str:
        return (
            f'ActorUnit(name:{self.name}, '
            f'health_max:{self.health_max}, '
            f'_health:{self._health}, '
            f'weapons:{repr(self.weapons)}, '
            f'armor:{repr(self.armor)}, '
            f'_xp:{self._xp}, '
            f'_lvl:{self._lvl}, '
            f'inventory:{self.inventory})'
        )


class Enemy(ActorUnit):
    """
    Class for all enemy units, extends ActorUnit.
    """

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5),
                 hostility: int = 555):

        super().__init__(name, health, starter_weapon, starter_armor)

        # Hostility towards the player.
        # 0-99:Friendly; 100-174:Neutral; 175-254:Disgruntled ; 255+:hostile
        self.hostility: int = hostility

        GameState.actors.append(self)

    def turn(self) -> None:
        if GameState.nonfree_action_taken:  # Non-free action with respect to the player
            GameState.round_count += 1
            self.attack()

    def weapon_selector(self) -> Weapon:
        chosen_index: int = -1
        index: int = 0
        dmg: float = 0
        for weapon in self.weapons:
            if weapon.dmg > dmg:  # AI always picks highest dmg weapon available.
                dmg = weapon.dmg
                chosen_index = index
            index += 1

        return self.weapons[chosen_index]

    def target_selector(self) -> 'ActorUnit':
        return GameState.player_actor

    def __str__(self) -> str:
        character_stat: str = (
            f'Name:    {self.name}\n'
            f'HP:      {self.health} / {self.health_max}\n'
            f'=====================================\n'
            f'Weapons\n'
            f'=====================================\n'
        )
        weapon_stat: str = ""
        for weapon in self.weapons:
            weapon_stat += str(weapon)
        armor_header: str = (
            f'=====================================\n'
            f'Armor\n'
            f'=====================================\n'
        )
        armor_stat: str = str(self.armor)
        return character_stat + weapon_stat + armor_header + armor_stat

    def __repr__(self) -> str:
        return (
            f'ActorUnit(name:{self.name}, '
            f'health_max:{self.health_max}, '
            f'_health:{self._health}, '
            f'weapons:{repr(self.weapons)}, '
            f'armor:{repr(self.armor)}, '
            f'hostility:{self.hostility}, '
            f'inventory:{self.inventory})'
        )


class Merchant(ActorUnit):
    """
    Shop/Merchant class, extends ActorUnit.
    """

    def __init__(self):
        super().__init__('Merchant')
        x: int = GameState.round_count
        self.inventory: Inventory = Inventory()
        self.inventory.gold = rand.randrange(10+x*5, 80+x*15)
