###################################
# Imports                         #
###################################


import random as rand
import uuid as uuid
import math as math


###################################
# Class Definitions               #
###################################


class GameObject:
    """

    """

    actors: list = []
    combat_help: str = 'Combat Help: (h)elp, (a)ttack, (p)ass, (s)tatus, hunt (e)nemy'
    combat_actions: dict = {
        'help': lambda *args, **kwargs: print(GameObject.combat_help),
        'h': lambda *args, **kwargs: print(GameObject.combat_help),
        'attack': lambda *args, **kwargs: kwargs['actor'].attack(),
        'a': lambda *args, **kwargs: kwargs['actor'].attack(),
        'pass': lambda *args, **kwargs: 0,
        'p': lambda *args, **kwargs: 0,
        'status': lambda *args, **kwargs: print(kwargs['actor']),
        's': lambda *args, **kwargs: print(kwargs['actor']),
        'hunt enemy': lambda *args, **kwargs: GameObject.Events.generate_enemy(),
        'e': lambda *args, **kwargs: GameObject.Events.generate_enemy(is_boss=True)
    }
    standard_help: str = 'Help: (h)elp, (s)tatus, sho(p), (r)epair, hunt (e)nemy'
    standard_actions: dict = {
        'help': lambda *args, **kwargs: print(GameObject.standard_help),
        'h': lambda *args, **kwargs: print(GameObject.standard_help),
        'status': lambda *args, **kwargs: print(kwargs['actor']),
        's': lambda *args, **kwargs: print(kwargs['actor']),
        'shop': '',
        'p': '',
        'repair': '',
        'r': '',
        'hunt enemy': lambda *args, **kwargs: GameObject.Events.generate_enemy(),
        'e': lambda *args, **kwargs: GameObject.Events.generate_enemy()

    }

    damage_types: list = ['Slicing', 'Piercing', 'Bludgeoning', 'Fire', 'Cold', 'Mental']
    turn_count: int = 0
    player_actor: 'ActorUnit' = None
    is_active_game: bool = True
    nonfree_action_taken: bool = False
    nonfree_actions: list = [
        'attack',
        'a',
        'hunt enemy',
        'e'
    ]
    enemy_count: int = 0
    merchant_present: bool = False
    merchant: 'Shop' = None

    def __init__(self):
        player_name = input('What is your name? ')
        GameObject.turn_count = 0
        GameObject.actors = []
        GameObject.is_active_game = True
        GameObject.nonfree_action_taken = False
        GameObject.enemy_count = 0
        GameObject.merchant_present = False

        # Player Init.
        weapon: Weapon = Weapon('Sword-like Catfish', 6, 25, 1, damage_type='Slicing')
        GameObject.player_actor = ActorUnit(name=player_name, health=20, starter_weapon=weapon, hostility=0)
        GameObject.player_actor.weapons.append(Weapon('Fists'))
        GameObject.actors.append(GameObject.player_actor)

        GameObject.Events.generate_enemy()

    @staticmethod
    def turn():
        print('\n-------------------------------------')
        if GameObject.player_actor.health < 1:
            print('Game Over')
            GameObject.is_active_game = False
            return
        for actor in GameObject.actors:
            if actor is GameObject.player_actor:
                while True:
                    user_command = input('Give your command: ').lower()
                    if GameObject.enemy_count != 0 and user_command in GameObject.combat_actions:
                        GameObject.combat_actions[user_command](actor=actor)
                        if user_command in GameObject.nonfree_actions:  # Enemies only attack if player does
                            GameObject.nonfree_action_taken = True
                        break
                    elif user_command in GameObject.standard_actions:
                        GameObject.standard_actions[user_command](actor=actor)
                        break
                    else:
                        print('Invalid command.')
                        continue
            else:  # actions to occur on every enemy turn
                if GameObject.nonfree_action_taken:
                    GameObject.turn_count += 1
                    actor.attack(target=GameObject.player_actor)
                    GameObject.Events.random_event()

        GameObject.nonfree_action_taken = False

    @staticmethod
    def reset():
        GameObject()

    class Events:
        @staticmethod
        def generate_enemy(is_boss: bool = False):
            x: int = GameObject.turn_count
            if is_boss:
                hp: int = int(15+x*0.5+x**2)
                atk: int = int(math.floor(x*0.8))
                dur: int = int(30+0.00003*x**3)
                hit_mod: int = int(math.floor(x*0.1))
                ranged: bool = True if rand.random() > 0.9 else False
                weapon: Weapon = Weapon('Whip of the North', atk, dur, hit_mod, 'Cold', is_ranged=ranged)
                default_weapon: Weapon = Weapon('Fists', 5, hit_modifier=2)

                res: str = GameObject.damage_types[rand.randrange(0, len(GameObject.damage_types))]
                armor: Armor = Armor('Heavy Chains', 50, [res], 3, 3)

                boss: ActorUnit = ActorUnit('Mantissa the Lightly-chilled', hp, weapon, armor, hostility=555)
                boss.weapons.append(default_weapon)

                print(f'{boss.name} has appeared!\n{boss}')
                GameObject.actors.append(boss)

            else:
                min_hp: int = int(3+(x**2)*0.009)
                max_hp: int = int(11+(x**2)*0.02)
                hp: int = rand.randint(min_hp, max_hp)
                atk: int = int()
                hit_mod: int = int(math.floor(x*0.06667))
                weapon: Weapon = Weapon('Spiked Club', atk, 15, hit_mod, 'Piercing')
                default_weapon: Weapon = Weapon('Fists')

                armor: Armor = Armor('Wooden Plate', 8, None, 2, 2)

                mob: ActorUnit = ActorUnit('Goblin', hp, weapon, armor, hostility=555)
                mob.weapons.append(default_weapon)

                print(f'A {mob.name} approaches.')
                GameObject.actors.append(mob)
            GameObject.enemy_count += 1

        @staticmethod
        def random_event():
            roll = rand.random()*100
            if roll < 50:
                pass
            elif roll < 60:
                GameObject.Events.generate_enemy()
            elif roll < 65:
                if GameObject.turn_count > 30:
                    GameObject.Events.generate_enemy(is_boss=True)
            else:
                pass


class Weapon:

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 damage: float = 1,
                 durability: int = 999,
                 hit_modifier: int = 0,
                 damage_type: str = 'Bludgeoning',
                 is_ranged: bool = False):

        Weapon._instance_count += 1

        self.name: str = name
        self._dmg: float = damage
        self.durability_max: int = durability
        self._durability: float = durability
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

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, new_durability: float):
        self._durability = new_durability
        if self._durability < 1:
            print(f'{self.name} has broken!')
            self._durability = 0

    @property
    def dmg(self):
        if self.durability < 1:
            return 1
        return self._dmg

    @dmg.setter
    def dmg(self, new_dmg: float):
        self._dmg = new_dmg

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

    def __repr__(self):
        return (
            f'Weapon(name:{self.name}, '
            f'_dmg:{self._dmg}, '
            f'durability_max: {self.durability_max}, '
            f'_durability: {self._durability}, '
            f'hit_mod: {self.hit_mod}, '
            f'dmg_type: {self.dmg_type}, '
            f'is_ranged: {self.is_ranged}'
                )

class Armor:

    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 durability: int = 999,
                 resistances=None,
                 defense: int = 0,
                 armor_class: int = 0):

        if resistances is None:
            resistances = []

        Armor._instance_count += 1

        self.name: str = name
        self.durability_max: int = durability
        self._durability: float = durability
        self._resistances: list = resistances
        self._defense: int = defense
        self.AC: int = armor_class  # Armor Class

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, new_durability: float):
        self._durability = new_durability
        if self._durability < 1:
            print(f'{self.name} has broken!')
            self._durability = 0

    @property
    def defense(self):
        if self.durability < 1:
            return 0
        return self._defense

    @defense.setter
    def defense(self, new_defense: float):
        self._defense = new_defense

    @property
    def resistances(self):
        if self.durability < 1:
            return []
        return self._resistances

    @resistances.setter
    def resistances(self, new_resistances: list):
        self._resistances = new_resistances

    def add_resistance(self, new_resistance: str):
        if new_resistance in GameObject.damage_types:
            self._resistances.append(new_resistance)
        else:
            raise ValueError('Not a valid resistance.')

    def __str__(self):
        x: str = (f'  {self.name}  \n'
                  f'++{"+"*len(self.name)}++\n'
                  f'Durability:  {self.durability} / {self.durability_max}\n'
                  f'Resistances: {", ".join(self.resistances)}\n'
                  f'Defense:     {self.defense}\n'
                  f'AC:          {self.AC}\n'
                  f'++{"+" * len(self.name)}++\n')
        return x


class ActorUnit:
    """

    """

    # Counts the amount of active units, potentially used for scaling
    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor(name='Loincloth', defense=2, armor_class=5),
                 level: int = 0,
                 experience: int = 1,
                 hostility: int = 170):

        ActorUnit._instance_count += 1

        self.name = name
        self.identifier = uuid.uuid4()

        self.health_max: int = health
        self._health: float = health
        self.weapons: list = [starter_weapon]
        self.armor: Armor = starter_armor

        self._xp: int = experience
        self._lvl: int = level

        # Hostility towards the player.
        # 0-99:Friendly; 100-174:Neutral; 175-254:Disgruntled ; 255+:hostile
        self.hostility: int = hostility

        self.inventory: list = []

    @staticmethod
    def unit_count() -> int:
        """
        Getter for the amount of ActorUnit instances alive.

        :return: Unit count stored in class (not per-instance).
        """
        return ActorUnit._instance_count

    def attack(self, **kwargs):
        if self is not GameObject.player_actor:  # Player vs. AI selection logic.
            target: ActorUnit = kwargs['target']  # AI
        else:
            target: ActorUnit = self.target_selector()  # Player

        weapon: Weapon = self.weapon_selector()

        if weapon.is_ranged:
            print('Try ranged battle; not implemented.')
        else:
            roll: int = rand.randint(1, 20)  # Chance to hit logic.
            if roll+weapon.hit_mod >= target.armor.AC:
                if roll < 8:  # 40% chance to lose 1 durability every attack.
                    weapon.durability -= 1
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

    def target_selector(self) -> 'ActorUnit':
        index = 0
        for actor in GameObject.actors:
            if actor is not self:
                print(f'ID-{index:02} | {actor.name}: HP-{actor.health} Def-{actor.armor.defense}\n'
                      f'      | {" "*(len(actor.name)+1)} AC-{actor.armor.defense} Res-{", ".join(actor.armor.resistances)}')
            else:
                banned_index = index
            index += 1
        chosen_index = -1
        while chosen_index <= 0 or index <= chosen_index != banned_index:
            try:
                chosen_index = int(input('Choose a valid target ID: '))
            except ValueError:
                print('Not a valid numeric ID.')
        return GameObject.actors[chosen_index]

    def weapon_selector(self) -> Weapon:
        index = 0
        chosen_index = -1
        if self is not GameObject.player_actor:  # AI
            dmg = 0
            for weapon in self.weapons:
                if weapon.dmg > dmg:  # AI always picks highest dmg weapon available.
                    dmg = weapon.dmg
                    chosen_index = index
                index += 1

        else:  # Player
            for weapon in self.weapons:
                print(f'ID-{index:02} | {weapon.name}: Dmg-{weapon.dmg} Type-{weapon.dmg_type}\n'
                      f'      | {" "*(len(weapon.name)+1)} Hit-+{weapon.hit_mod} Dur-{weapon.durability}/{weapon.durability_max}\n'
                      f'      | {" "*(len(weapon.name)+1)} Ranged-{"Yes" if weapon.is_ranged else "No"}')
                index += 1
            while chosen_index < 0 or index <= chosen_index:
                try:
                    chosen_index = int(input('Choose a valid weapon ID: '))
                except ValueError:
                    print('Not a valid numeric ID.')
        return self.weapons[chosen_index]

    def don_armor(self, new_armor: 'Armor'):
        pass

    @property
    def armor_durability(self) -> float:
        return self.armor.durability

    @armor_durability.setter
    def armor_durability(self, new_durability: float):
        self.armor.durability = new_durability
        if self.armor.durability < 1:
            self.armor = Armor()  # When armor breaks, equip loincloth

    def modify_weapon_durability(self, weapon: Weapon, durability_delta: float):
        if weapon in self.weapons:
            weapon.durability += durability_delta
            if weapon.durability < 1:
                self.weapons.remove(weapon)
        else:
            raise ValueError(f'{repr(self)} does not own this weapon: {repr(self)}')

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, new_health: int):
        self._health = new_health
        if self._health <= 0:
            print(f'{self.name} has been slain. (Overkill: {abs(self._health)})')
            for actor in GameObject.actors:
                if actor is self and actor is not GameObject.player_actor:
                    GameObject.actors.remove(actor)
                    if actor.hostility > 254:
                        GameObject.enemy_count -= 1

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
            f''
        )


class Shop:

    def __init__(self):
        x: int = GameObject.turn_count
        self.gold = rand.randrange(10+x*5, 80+x*15)


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


