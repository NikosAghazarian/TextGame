import random as rand

from TextGame.GameState import GameState
from TextGame.UnitTypes import Enemy
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

        :param is_boss: Controls whether to spawn a standard mob or a boss mob.
        """

        x: int = GameState.round_count  # Scaling variable.
        if is_boss:
            # Boss Stat Block
            x += x * 0.1
            hp: int = int(15 + x * 0.5 + 0.02 * x**2)  # Quadratic

            weapon: Weapon = Weapon.weapon_gen(x)
            default_weapon: Weapon = Weapon('Fists', 5, hit_modifier=2)
            armor: Armor = Armor.armor_gen(x)

            boss: Enemy = Enemy('Mantissa the Lightly-chilled', hp, weapon, armor, x)
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
            armor: Armor = Armor.armor_gen(x)

            mob: Enemy = Enemy('Goblin', hp, weapon, armor, x)
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
            if GameState.round_count > 30:
                Events.generate_enemy(is_boss=True)
                return True
        else:
            return False
