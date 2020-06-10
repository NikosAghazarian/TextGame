###################################
# Imports                         #
###################################


import random as rand
import uuid as uuid


###################################
# Class Definitions               #
###################################


class GameObject:
    """

    """

    actors: list = []
    actions: dict = {'help': lambda *args, **kwargs: print('(h)elp, (a)ttack, (p)ass'),
                     'h': lambda *args, **kwargs: print('(h)elp, (a)ttack, (p)ass'),
                     'attack': lambda *args, **kwargs: kwargs['actor'].attack(),
                     'a': lambda *args, **kwargs: kwargs['actor'].attack(),
                     'pass': lambda *args, **kwargs: 0,
                     'p': lambda *args, **kwargs: 0
                     }
    turn_count: int = 0
    player_actor = 0
    is_active_game: bool = True

    def __init__(self):
        player_name = input('What is your name? ')
        GameObject.turn_count = 0
        GameObject.actors = []
        GameObject.is_active_game = True
        GameObject.player_actor: ActorUnit = ActorUnit(name=player_name, health=20)
        GameObject.actors.append(GameObject.player_actor)

    @staticmethod
    def turn():
        if GameObject.player_actor.health == 0:
            print('Game Over')
            GameObject.is_active_game = False
            return
        GameObject.turn_count += 1
        for actor in GameObject.actors:
            if actor is GameObject.player_actor:
                while True:
                    user_command = input('Give your command: ').lower()
                    if user_command in GameObject.actions:
                        GameObject.actions[user_command](actor=actor)
                        break
                    else:
                        print('Invalid command.')
                        continue
            else:
                actor.attack(target=GameObject.player_actor)
        GameObject.generate_enemy()

    @staticmethod
    def reset():
        GameObject.__init__()

    @staticmethod
    def generate_enemy():
        GameObject.actors.append(ActorUnit(health=rand.randint(3, 11)))

    def __str__(self):
        return self


class ActorUnit:
    """

    """
    # Counts the amount of active units, potentially used for scaling
    _instance_count = 0

    def __init__(self, name: str = 'default', health: int = 1, defense: int = 0, armor_class: int = 0):

        ActorUnit._instance_count += 1

        self.name = name
        self.identifier = uuid.uuid4()

        self.health_max: int = health
        self._health: float = health
        self.defense: int = defense
        self.AC: int = armor_class  # Armor Class
        self.weapon = Weapon(damage=5)

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: Unit count stored in class (not per-instance).
        """
        return ActorUnit._instance_count

    def attack(self, **kwargs):
        if self is not GameObject.player_actor:
            target: ActorUnit = kwargs['target']
        else:
            target: ActorUnit = self.target_selector()

        if self.weapon.is_ranged:
            pass
        else:
            print(f'{self.name} hit {target.name} for {self.weapon.dmg}')
            target.health -= self.weapon.dmg

    def take_damage(self, damage: float, damage_type: str):
        pass

    def target_selector(self) -> 'ActorUnit':
        index = 0
        for actor in GameObject.actors:
            if actor is not self:
                print(f'ID-{index:02} | {actor.name}: HP-{actor.health}')
            else:
                banned_index = index
            index += 1
        chosen_index = -1
        while chosen_index < 0 or index <= chosen_index != banned_index:
            try:
                chosen_index = int(input('Choose a valid target ID: '))
            except ValueError:
                print("Not a valid numeric ID.")
        return GameObject.actors[chosen_index]

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        self._health = new_health
        if self._health <= 0:
            print(f'{self.name} has been slain. (Overkill: {abs(self._health)})')
            for actor in GameObject.actors:
                if actor is self:
                    GameObject.actors.remove(actor)


#    def __str__(self):
#       return self


class Weapon:

    _instance_count = 0

    def __init__(self,
                 damage: float = 1,
                 durability: int = 1,
                 hit_modifier: int = 0,
                 damage_type: str = 'Slicing',
                 is_ranged: bool = False):

        Weapon._instance_count += 1

        self.dmg: float = damage
        self.durability_max: int = durability
        self.durability: float = durability
        self.hit_mod: int = hit_modifier
        self.dmg_type: str = damage_type
        self.is_ranged: bool = is_ranged

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: Unit count stored in class (not per-instance).
        """
        return Weapon._instance_count


###################################
# Code Execution                  #
###################################


rand.seed()

GameObject()

while True:
    GameObject.turn()
    if not GameObject.is_active_game:
        user_continue = input("Continue? [Y/n]").lower()
        if user_continue == "y":
            GameObject.reset()
        elif user_continue == "n":
            break
        else:
            continue


