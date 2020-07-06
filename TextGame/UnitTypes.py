import random as rand

from TextGame.GameState import GameState
from TextGame.Inventory import Inventory
from TextGame.ActorUnit import ActorUnit
from TextGame.Armor import Armor
from TextGame.Weapon import Weapon
from TextGame.Menu import Menu


class Player(ActorUnit):

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5),
                 level: int = 0,
                 experience: int = 1):

        super().__init__(name, health, starter_weapon, starter_armor, level, experience)

    def turn(self):
        if self.isPlayer:
            Menu.menu_logic()
        else:  # actions to occur on every enemy turn
            if GameState.nonfree_action_taken:
                GameState.round_count += 1
                self.attack()

class Enemy(ActorUnit):

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5),
                 level: int = 0,
                 experience: int = 1,
                 hostility: int = 555):

        super().__init__(name, health, starter_weapon, starter_armor, level, experience)
        self.hostility: int = hostility


class Merchant(ActorUnit):
    """
    Shop/Merchant class, extends ActorUnit.
    """

    def __init__(self):
        super().__init__('Merchant', )
        x: int = GameState.round_count
        self.inventory: Inventory = Inventory()
        self.inventory.gold = rand.randrange(10+x*5, 80+x*15)
