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
    actions: dict = {'help': lambda *args, **kwargs: print('(h)elp, (a)ttack, (p)ass, (s)tatus'),
                     'h': lambda *args, **kwargs: print('(h)elp, (a)ttack, (p)ass, (s)tatus'),
                     'attack': lambda *args, **kwargs: kwargs['actor'].attack(),
                     'a': lambda *args, **kwargs: kwargs['actor'].attack(),
                     'pass': lambda *args, **kwargs: 0,
                     'p': lambda *args, **kwargs: 0,
                     'status': lambda *args, **kwargs: print(kwargs['actor']),
                     's': lambda *args, **kwargs: print(kwargs['actor'])
                     }
    turn_count: int = 0
    player_actor = 0
    is_active_game: bool = True
    nonfree_action_taken: bool = False
    nonfree_actions: list = [
        'attack',
        'a'
    ]

    def __init__(self):
        player_name = input('What is your name? ')
        GameObject.turn_count = 0
        GameObject.actors = []
        GameObject.is_active_game = True
        GameObject.nonfree_action_taken = False
        GameObject.player_actor: ActorUnit = ActorUnit(name=player_name, health=20)
        GameObject.actors.append(GameObject.player_actor)

    @staticmethod
    def turn():
        print('\n')
        if GameObject.player_actor.health < 1:
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
                        if user_command in GameObject.nonfree_actions:  # Enemies only attack if player does
                            GameObject.nonfree_action_taken = True
                        break
                    else:
                        print('Invalid command.')
                        continue
            else:  # actions to occur on every enemy turn
                if GameObject.nonfree_action_taken:
                    actor.attack(target=GameObject.player_actor)

        GameObject.nonfree_action_taken = False
        GameObject.generate_enemy()

    @staticmethod
    def reset():
        GameObject()

    @staticmethod
    def generate_enemy():
        min_hp: float = +GameObject.turn_count*0.1
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
        self.weapons: list = [Weapon(name='Short Sword of Beginners', damage=5)]
        self.armor: Armor = Armor(name='Loincloth', defense=2, armor_class=5)
        self.inventory: list = []

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

        if self.weapons[0].is_ranged:
            pass
        else:
            roll: int = rand.randint(1, 20)
            if roll+self.weapons[0].hit_mod >= target.armor.AC:
                print(f'{self.name} hit {target.name} for ', end='')
                target.take_damage(self.weapons[0].dmg, self.weapons[0].dmg_type)

    def take_damage(self, damage: float, damage_type: str):
        effective_dmg: float = damage
        if damage_type in self.armor.resistances:
            effective_dmg *= 0.66
        effective_dmg -= self.armor.defense

        print(f'{effective_dmg}')
        self.health -= effective_dmg

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

    def don_armor(self, new_armor: 'Armor'):
        pass

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_health):
        self._health = new_health
        if self._health <= 0:
            print(f'{self.name} has been slain. (Overkill: {abs(self._health)})')
            for actor in GameObject.actors:
                if actor is self and actor is not GameObject.player_actor:
                    GameObject.actors.remove(actor)

    def __str__(self):
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


class Weapon:

    _instance_count = 0

    damage_types: list = ['Slicing', 'Piercing', 'Bludgeoning', 'Fire', 'Cold', 'Mental']

    def __init__(self,
                 name: str = 'default',
                 damage: float = 1,
                 durability: int = 1,
                 hit_modifier: int = 0,
                 damage_type: str = 'Slicing',
                 is_ranged: bool = False):

        Weapon._instance_count += 1

        self.name: str = name
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

    def __str__(self):
        x: str = (f'  {self.name}  \n'
                  f'++{"+"*len(self.name)}++\n'
                  f'Dmg:          {self.dmg}\n'
                  f'Durability:   {self.durability} / {self.durability_max}\n'
                  f'To-Hit Bonus: +{self.hit_mod}\n'
                  f'Dmg Type:     {self.dmg_type}\n'
                  f'Ranged:       {"Yes" if self.is_ranged else "No"}\n'
                  f'++{"+" * len(self.name)}++\n'
                  )
        return x


class Armor:

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 durability: int = 1,
                 resistances=None,
                 defense: int = 0,
                 armor_class: int = 0):

        if resistances is None:
            resistances = ['Cold']

        Armor._instance_count += 1

        self.name: str = name
        self.durability_max: int = durability
        self.durability: float = durability
        self.resistances: list = resistances
        self.defense: int = defense
        self.AC: int = armor_class  # Armor Class

    def __str__(self):
        x: str = (f'  {self.name}  \n'
                  f'++{"+"*len(self.name)}++\n'
                  f'Durability:  {self.durability} / {self.durability_max}\n'
                  f'Resistances: {", ".join(self.resistances)}\n'
                  f'Defense:     {self.defense}\n'
                  f'AC:          {self.AC}\n'
                  f'++{"+" * len(self.name)}++\n')
        return x


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


