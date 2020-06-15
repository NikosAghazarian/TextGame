import random as rand

from TextGame.GameState import GameState
from TextGame.Menu import Menu
from TextGame.Armor import Armor
from TextGame.Weapon import Weapon
from TextGame.Inventory import Inventory


class ActorUnit:
    """
    Represents any and all controllable and non-controllable entities.
    """

    # Counts the amount of active units, potentially used for scaling
    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5),
                 level: int = 0,
                 experience: int = 1,
                 hostility: int = 170):

        ActorUnit._instance_count += 1

        self.name = name

        self.health_max: int = health
        self._health: float = health
        self.weapons: list = [starter_weapon]
        self.armor: Armor = starter_armor

        self._xp: int = experience
        self._lvl: int = level

        # Hostility towards the player.
        # 0-99:Friendly; 100-174:Neutral; 175-254:Disgruntled ; 255+:hostile
        self.hostility: int = hostility

        self.inventory: Inventory = Inventory()

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: Unit count stored in class (not per-instance).
        """
        return ActorUnit._instance_count

    def attack(self, target: 'ActorUnit' = None):
        if self is not GameState.player_actor:  # Player vs. AI selection logic.
            target: ActorUnit = target  # AI
        else:
            target: ActorUnit = self.target_selector()  # Player

        weapon: Weapon = self.weapon_selector()

        if weapon.is_ranged:
            print('Try finger; ranged battle not implemented.')
        else:
            roll: int = rand.randint(1, 20)  # Chance to hit logic.
            if roll+weapon.hit_mod >= target.armor.AC:
                if roll < 8:  # 40% chance to lose 1 durability every attack.
                    self.modify_weapon_durability(weapon, -1)
                print(f'{self.name} hit {target.name} with {weapon.name}+{weapon.hit_mod} for ', end='')
                target.take_damage(weapon.dmg, weapon.dmg_type)
            else:
                print(f'{self.name} missed!')

    def take_damage(self, damage: float, damage_type: str):
        effective_dmg: float = damage
        if damage_type in self.armor.resistances:
            effective_dmg *= 0.66  # Resistance grants 33% dmg reduction.
        effective_dmg -= self.armor.defense
        if effective_dmg < 1:  # Minimum 1 damage on hit
            effective_dmg = 1

        print(f'{effective_dmg} {damage_type.lower()} damage.')
        self.health -= effective_dmg

        armor_damage: float = effective_dmg - self.armor.defense
        if armor_damage < 0:  # EffDmg. - 2 * defense durability reduction.
            armor_damage = 0
        self.armor_durability -= armor_damage

    def target_selector(self) -> 'ActorUnit':
        banned_index = Menu.targeting(self)

        chosen_index: int = -1
        max_index: int = len(GameState.actors)-1
        while chosen_index <= 0 or max_index < chosen_index or chosen_index == banned_index:
            try:
                chosen_index = int(input('Choose a valid target ID: '))
            except ValueError:
                print('Not a valid numeric ID.')
        return GameState.actors[chosen_index]

    def weapon_selector(self) -> Weapon:
        chosen_index: int = -1

        if self is not GameState.player_actor:  # AI
            index: int = 0
            dmg: float = 0
            for weapon in self.weapons:
                if weapon.dmg > dmg:  # AI always picks highest dmg weapon available.
                    dmg = weapon.dmg
                    chosen_index = index
                index += 1
        else:  # Player
            Menu.player_weapons()
            max_index: int = len(self.weapons)-1
            while chosen_index < 0 or chosen_index > max_index:
                try:
                    chosen_index = int(input('Choose a valid weapon ID: '))
                except ValueError:
                    print('Not a valid numeric ID.')

        return self.weapons[chosen_index]

    def armor_selector(self) -> Armor:
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

    def don_armor(self):
        new_armor: Armor = self.armor_selector()
        if new_armor.durability >= 1:  # Check if broken.
            self.inventory.store(self.armor)  # Store current armor.
            self.inventory.retrieve(new_armor)  # Take out new armor.
            self.armor = new_armor  # Equip.
        else:
            print('This armor is too damaged to use.')

    def heal(self):
        """
        Heal action of player.

        :return:
        """
        self.health += 3

    def repair(self):
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

    def shop(self):

        Menu.shop()

    @property
    def armor_durability(self) -> float:
        return self.armor.durability

    @armor_durability.setter
    def armor_durability(self, new_durability: float):
        self.armor.durability = new_durability
        if self.armor.durability < 1:
            self.inventory.store(self.armor)  # Store current armor.
            self.armor = Armor('Loincloth', defense=2, armor_class=5)  # When armor breaks, equip loincloth

    def modify_weapon_durability(self, weapon: Weapon, durability_delta: float):
        if weapon in self.weapons:
            weapon.durability += durability_delta
            if weapon.durability < 1:
                self.weapons.remove(weapon)
        else:
            raise ValueError(f'{repr(self)} does not own this weapon: {repr(self)}')

    @property
    def health(self) -> float:
        """
        Getter for _health.

        :return: _health property of ActorUnit instance.
        """
        return self._health

    @health.setter
    def health(self, new_health: int):
        """
        Setter for _health.

        :param new_health: Set value.
        :return: None
        """
        self._health = new_health
        if self._health <= 0:
            print(f'{self.name} has been slain. (Overkill: {abs(self._health)})')
            ActorUnit._instance_count -= 1
            if self is not GameState.player_actor:
                GameState.actors.remove(self)
                if self.hostility > 254:
                    GameState.player_actor._xp += self._xp  # CHANGE THIS AFTER ADDING LEVELING
                    GameState.enemy_count -= 1

            else:
                print("You have died...")

        if self._health > self.health_max:
            self._health = self.health_max
            print('Fully healed!')

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
            f'_xp:{self._xp}, '
            f'_lvl:{self._lvl}, '
            f'hostility:{self.hostility}, '
            f'inventory:{self.inventory})'
        )
