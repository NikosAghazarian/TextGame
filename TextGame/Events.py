import math as math
import random as rand

from TextGame.GameState import GameState
from TextGame.ActorUnit import ActorUnit
from TextGame.Armor import Armor
from TextGame.Weapon import Weapon


class Events:
    """
    Container class for game events. Used for namespace cleanliness.
    """

    @staticmethod
    def generate_enemy(is_boss: bool = False) -> None:
        """
        Generates an enemy actor with stats scaled with GameObject.turn_count.

        TODO: Move Actor stat gen. to new file for scalability. Move gear stat gen. to respective classes.

        :param is_boss: Controls whether to spawn a standard mob or a boss mob.
        """

        x: int = GameState.turn_count  # Scaling variable.
        if is_boss:
            # Boss Stat Block
            x += 3
            hp: int = int(15 + x * 0.5 + 0.02 * x**2)  # Quadratic

            weapon: Weapon = Weapon.weapon_gen(x)
            default_weapon: Weapon = Weapon('Fists', 5, hit_modifier=2)

            res: str = GameState.damage_types[rand.randrange(0, len(GameState.damage_types))]  # Picks a random resistance
            armor: Armor = Armor('Heavy Chains', 50, [res], 3, 3)

            boss: ActorUnit = ActorUnit('Mantissa the Lightly-chilled', hp, weapon, armor, hostility=555)
            boss.weapons.append(default_weapon)

            print(f'{boss.name} has appeared!\n{boss}')
            GameState.actors.append(boss)

        else:
            # Mob Stat Block
            min_hp: int = int(3+(x**2)*0.009)
            max_hp: int = int(11+(x**2)*0.02)
            hp: int = rand.randint(min_hp, max_hp)
            weapon: Weapon = Weapon.weapon_gen(x)
            default_weapon: Weapon = Weapon('Fists')

            armor: Armor = Armor('Wooden Plate', 8, None, 2, 2)

            mob: ActorUnit = ActorUnit('Goblin', hp, weapon, armor, hostility=555)
            mob.weapons.append(default_weapon)

            print(f'A {mob.name.lower()} approaches.')
            GameState.actors.append(mob)
        GameState.enemy_count += 1

    @staticmethod
    def random_event() -> bool:
        """
        Rolls for a random game event.

        :return: True if event occurs, otherwise returns False.
        """
        roll: float = rand.random()*100
        if roll < 50:
            return False
        elif roll < 60:
            Events.generate_enemy()
            return True
        elif roll < 65:
            if GameState.turn_count > 30:
                Events.generate_enemy(is_boss=True)
                return True
        else:
            return False
