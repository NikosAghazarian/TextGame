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
    Singleton class that manages game-globals.
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
        'e': lambda *args, **kwargs: GameObject.Events.generate_enemy()
    }
    standard_help: str = 'Help: (h)elp, (s)tatus, sho(p), (r)epair, hunt (e)nemy, hea(l)'
    standard_actions: dict = {
        'help': lambda *args, **kwargs: print(GameObject.standard_help),
        'h': lambda *args, **kwargs: print(GameObject.standard_help),
        'status': lambda *args, **kwargs: print(kwargs['actor']),
        's': lambda *args, **kwargs: print(kwargs['actor']),
        'shop': '',
        'p': '',
        'repair': lambda *args, **kwargs: kwargs['actor'].repair(),
        'r': lambda *args, **kwargs: kwargs['actor'].repair(),
        'hunt enemy': lambda *args, **kwargs: GameObject.Events.generate_enemy(),
        'e': lambda *args, **kwargs: GameObject.Events.generate_enemy(),
        'heal': lambda *args, **kwargs: kwargs['actor'].heal(),
        'l': lambda *args, **kwargs: kwargs['actor'].heal()
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
        """
        Takes turns sequentially for each actor.

        TODO: Refactor in/out-of-combat logic into a decorator for actor actions.

        :return: None
        """
        print('\n-------------------------------------')
        if GameObject.player_actor.health < 1:  # Loss Condition
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
        """
        Container class for game events. Used for namespace cleanliness.
        """

        @staticmethod
        def generate_enemy(is_boss: bool = False):
            """
            Generates an enemy actor with stats controlled by GameObject.turn_count.

            :param is_boss: Controls whether to spawn a std. mob or a boss mob.
            :return: None
            """
            x: int = GameObject.turn_count
            if is_boss:
                # Boss Stat Block
                hp: int = int(15+x*0.5+x**2)
                atk: int = int(math.floor(1+x*0.8))
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
                GameObject.actors.append(mob)
            GameObject.enemy_count += 1

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
                GameObject.Events.generate_enemy()
                return True
            elif roll < 65:
                if GameObject.turn_count > 30:
                    GameObject.Events.generate_enemy(is_boss=True)
                    return True
            else:
                return False


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
    def durability(self) -> float:
        """
        Getter for _durability.

        :return: _durability.
        """
        return self._durability

    @durability.setter
    def durability(self, new_durability: float):
        """
        Setter for _durability. Contains logic for breakage and negative(invalid) durabilities.
        Also contains logic for excess repair.

        :param new_durability: New value.
        :return: None
        """
        self._durability = new_durability
        if self._durability < 1:
            print(f'{self.name} has broken!')
            self._durability = 0
        elif self._durability > self.durability_max:
            self._durability = self.durability_max
            print(f'{self.name} is fully repaired!')

    @property
    def dmg(self) -> float:
        """
        Getter for _dmg with logic for broken weapons.

        :return: If durability is 0, returns 1, otherwise returns _dmg.
        """
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
            f'is_ranged: {self.is_ranged})'
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
        elif self._durability > self.durability_max:
            self._durability = self.durability_max
            print(f'{self.name} is fully repaired!')

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

    def __repr__(self) -> str:
        return (
            f'Armor(name:{self.name}, '
            f'durability_max:{self.durability_max}, '
            f'_durability:{self._durability}, '
            f'_resistances:{self._resistances}, '
            f'_defense:{self._defense}, '
            f'AC:{self.AC})'
        )


class ActorUnit:
    """

    """

    # Counts the amount of active units, potentially used for scaling
    _instance_count = 0

    def __init__(self,
                 name: str = 'default',
                 health: int = 1,
                 starter_weapon: Weapon = Weapon('Fists'),
                 starter_armor: Armor = Armor('Loincloth', defense=2, armor_class=5),
                 level: int = 0,
                 experience: int = 1,
                 hostility: int = 170):

        ActorUnit._instance_count += 1

        self.name = name

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
            print('Try finger; ranged battle not implemented.')
        else:
            roll: int = rand.randint(1, 20)  # Chance to hit logic.
            if roll+weapon.hit_mod >= target.armor.AC:
                if roll < 8:  # 40% chance to lose 1 durability every attack.
                    self.modify_weapon_durability(weapon, -1)
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

        armor_damage: float = effective_dmg - self.armor.defense
        if armor_damage < 0:
            armor_damage = 0
        self.armor_durability -= armor_damage

        print(f'{effective_dmg} {damage_type.lower()} damage.')
        self.health -= effective_dmg

    def target_selector(self) -> 'ActorUnit':
        index: int = 0
        chosen_index: int = -1

        for actor in GameObject.actors:
            if actor is not self:
                print(f'ID-{index:02} | {actor.name}: HP-{actor.health} Def-{actor.armor.defense}\n'
                      f'      | {" "*(len(actor.name)+1)} AC-{actor.armor.defense} Res-{", ".join(actor.armor.resistances)}')
            else:
                banned_index: int = index
            index += 1
        while chosen_index <= 0 or index <= chosen_index != banned_index:
            try:
                chosen_index = int(input('Choose a valid target ID: '))
            except ValueError:
                print('Not a valid numeric ID.')
        return GameObject.actors[chosen_index]

    def weapon_selector(self) -> Weapon:
        index: int = 0
        chosen_index: int = -1

        if self is not GameObject.player_actor:  # AI
            dmg: float = 0
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

    def armor_selector(self) -> Armor:
        index: int = 0
        chosen_index: int = -1
        armors: list = [self.armor]
        armors.extend([item for item in self.inventory if type(item) == 'Armor'])
        for armor in armors:
            print(f'ID-{index:02} | {armor.name}: Def-{armor.defense} AC-{armor.AC}\n'
                  f'      | {" "*(len(armor.name)+1)} Dur-{armor.durability}/{armor.durability_max} Res-{", ".join(armor.resistances)}\n'
                  )
            index += 1
        while chosen_index < 0 or index <= chosen_index:
            try:
                chosen_index = int(input('Choose a valid weapon ID: '))
            except ValueError:
                print('Not a valid numeric ID.')
        return armors[chosen_index]

    def don_armor(self):
        new_armor: Armor = self.armor_selector()
        if new_armor.durability >= 1:  # Check if broken.
            self.inventory.append(self.armor)  # Store current armor.
            self.inventory.remove(new_armor)  # Take out new armor.
            self.armor = new_armor  # Equip.
        else:
            print('This armor is too damaged to use.')

    def heal(self):
        """
        Heal action of player.

        :return:
        """
        self.health += 3

    def repair(self):
        """
        Repair player equipment.

        :return: None
        """
        command = ''
        while command not in ['a', 'armor', 'w', 'weapon']:
            command = input('Repair (A)rmor or (W)eapon: ').lower()

        if command in ['a', 'armor']:
            item: Armor = self.armor_selector()
            item.durability += item.durability_max * 0.05
        elif command in ['w', 'weapon']:
            item: Weapon = self.weapon_selector()
            self.modify_weapon_durability(item, item.durability_max * 0.05)
        else:
            raise ValueError('Not sure how you got here.')
        print(f'{item.name}: {item.durability} / {item.durability_max}')



    @property
    def armor_durability(self) -> float:
        return self.armor.durability

    @armor_durability.setter
    def armor_durability(self, new_durability: float):
        self.armor.durability = new_durability
        if self.armor.durability < 1:
            self.inventory.append(self.armor)  # Store current armor.
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
        """
        Getter for _health.

        :return: _health property of ActorUnit instance.
        """
        return self._health

    @health.setter
    def health(self, new_health: int):
        """
        Setter for _health.

        :param new_health: Set value.
        :return: None
        """
        self._health = new_health
        if self._health <= 0:
            print(f'{self.name} has been slain. (Overkill: {abs(self._health)})')
            for actor in GameObject.actors:
                if actor is self and actor is not GameObject.player_actor:
                    GameObject.actors.remove(actor)
                    if actor.hostility > 254:
                        GameObject.enemy_count -= 1
        if self._health > self.health_max:
            self._health = self.health_max
            print('Fully healed!')

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
            f'ActorUnit(name:{self.name}, '
            f'health_max:{self.health_max}, '
            f'_health:{self._health}, '
            f'weapons:{repr(self.weapons)}, '
            f'armor:{repr(self.armor)}, '
            f'_xp:{self._xp}, '
            f'_lvl:{self._lvl}, '
            f'hostility:{self.hostility}'
            f'inventory:{self.inventory})'
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


