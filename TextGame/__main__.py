import fraction as fraction
from fractions import Fraction
import random as rand

rand.seed

class GameObject:
    """

    """

    def __init__(self):
        self.turn_count: int = 0
        self.player_actor: ActorUnit = ActorUnit(rand.randint())


class ActorUnit:
    """

    """
    _unit_count = 0

    def __init__(self, health: int, ):
        ActorUnit._unit_count += 1
        self.health: fraction = Fraction(health, health)
        self.armor: int = 0