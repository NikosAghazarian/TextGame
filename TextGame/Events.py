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

        scaling: int = GameState.player_actor.lvl  # Scaling variable.
        if is_boss:
            # Boss Stat Block
            scaling += scaling * 0.1
            hp: int = int(15 + scaling * 0.5 + 0.02 * scaling ** 2)  # Quadratic

            weapon: Weapon = Weapon.weapon_gen(scaling)
            default_weapon: Weapon = Weapon('Fists', 5, hit_modifier=2)
            armor: Armor = Armor.armor_gen(scaling)

            boss: Enemy = Enemy('Mantissa the Lightly-chilled', hp, weapon, armor)
            boss.weapons.append(default_weapon)

            print(f'{boss.name} has appeared!\n{boss}')

        else:
            # Mob Stat Block
            min_hp: int = int(3+(scaling**2)*0.009)
            max_hp: int = int(11+(scaling**2)*0.02)
            hp: int = rand.randint(min_hp, max_hp)

            weapon: Weapon = Weapon.weapon_gen(scaling)
            default_weapon: Weapon = Weapon('Fists')
            armor: Armor = Armor.armor_gen(scaling)

            mob: Enemy = Enemy('Goblin', hp, weapon, armor)
            mob.weapons.append(default_weapon)

            print(f'A {mob.name.lower()} approaches.')

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
            if GameState.player_actor.lvl > 15:
                Events.generate_enemy(is_boss=True)
                return True
            return False
        else:
            return False
