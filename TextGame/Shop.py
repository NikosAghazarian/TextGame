import random as rand

from TextGame.GameState import GameState
from TextGame.Inventory import Inventory
from TextGame.ActorUnit import ActorUnit


class Shop(ActorUnit):

    def __init__(self):
        x: int = GameState.turn_count
        self.inventory: Inventory = Inventory()
        self.inventory.gold = rand.randrange(10+x*5, 80+x*15)
