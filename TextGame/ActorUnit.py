import random as rand
import math as math

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
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5)
                 ):

        ActorUnit._instance_count += 1

        self.name: str = name
        self.isPlayer: bool = False

        self.health_max: int = health
        self._health: float = health
        self.weapons: list = [starter_weapon]
        self.armor: Armor = starter_armor

        self.inventory: Inventory = Inventory()

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: Unit count stored in class (not per-instance).
        """
        return ActorUnit._instance_count

    def turn(self):
        if self.isPlayer:
            Menu.menu_logic()
        else:  # actions to occur on every enemy turn
            if GameState.nonfree_action_taken:

                self.attack()

    def attack(self):
        target: ActorUnit = self.target_selector()  # Player
        weapon: Weapon = self.weapon_selector()

        if weapon.is_ranged:
            print('Fah Losei Dovahkiin; ranged battle not implemented.')
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

    @property
    def armor_durability(self) -> float:
        return self.armor.durability

    @armor_durability.setter
    def armor_durability(self, new_durability: float):
        self.armor.durability = new_durability
        if self.armor.durability < 1:
            self.inventory.store(self.armor)  # Store current armor.
            self.armor = Armor('Loincloth', defense=2, armor_class=5)  # When armor breaks, equip loincloth

    def modify_weapon_durability(self, weapon: Weapon, durability_delta: float) -> None:
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
                GameState.player_actor.xp += math.ceil(0.13*self.health_max)  # CHANGE THIS AFTER ADDING LEVELING
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
            f'inventory:{self.inventory})'
        )
