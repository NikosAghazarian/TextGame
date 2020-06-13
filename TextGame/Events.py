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
    def generate_enemy(is_boss: bool = False):
        """
        Generates an enemy actor with stats scaled with GameObject.turn_count.

        TODO: Move Actor stat gen. to new file for scalability. Move gear stat gen. to respective classes.

        :param is_boss: Controls whether to spawn a standard mob or a boss mob.
        :return: None
        """
        x: int = GameState.turn_count
        if is_boss:
            # Boss Stat Block
            hp: int = int(15+x*0.5+x**2)  # Quadratic

            atk: int = int(math.floor(1+x*0.8))  # Linear
            dur: int = int(30+0.00003*x**3)  # Cubic, but very slow start
            hit_mod: int = int(math.floor(x*0.1))  # Linear monotonic step.
            ranged: bool = True if rand.random() > 0.9 else False  # 10% chance for ranged battle.
            weapon: Weapon = Weapon('Whip of the North', atk, dur, hit_mod, 'Cold', is_ranged=ranged)
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
            atk: int = int(math.floor(1+x*0.7))
            hit_mod: int = int(math.floor(x*0.06667))
            weapon: Weapon = Weapon('Spiked Club', atk, 15, hit_mod, 'Piercing')
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

        :return: True is event occurs, otherwise returns False.
        """
        roll = rand.random()*100
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
