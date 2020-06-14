from TextGame.GameState import GameState


class Menu:
    """
    Namespace class
    """

    @staticmethod
    def menu_logic():
        while True:
            user_command = input('Give your command: ').lower()

            if GameState.enemy_count != 0 and user_command in Menu.Actions.combat_actions:  # Combat Menu.
                Menu.Actions.combat_actions[user_command]()
                if user_command in Menu.Actions.nonfree_actions:  # Enemies only attack if player does.
                    GameState.nonfree_action_taken = True
                break
            elif user_command in Menu.Actions.noncombat_actions:  # Non-combat Menu.
                Menu.Actions.noncombat_actions[user_command]()
                break
            else:
                print('Invalid command.')
                continue

    @staticmethod
    def targeting(attacker: 'ActorUnit') -> int:
        index: int = 0
        banned_index: int = 1
        for actor in GameState.actors:
            if actor is not attacker:
                print(f'ID-{index:02} | {actor.name}: HP-{actor.health} Def-{actor.armor.defense}\n'
                      f'      | {" " * (len(actor.name) + 1)} AC-{actor.armor.defense} Res-{", ".join(actor.armor.resistances)}')
            else:
                banned_index: int = index
            index += 1
        return banned_index

    @staticmethod
    def player_weapons():
        index: int = 0
        for weapon in GameState.player_actor.weapons:
            print(f'ID-{index:02} | {weapon.name}: Dmg-{weapon.dmg} Type-{weapon.dmg_type}\n'
                  f'      | {" " * (len(weapon.name) + 1)} Hit-+{weapon.hit_mod} Dur-{weapon.durability}/{weapon.durability_max}\n'
                  f'      | {" " * (len(weapon.name) + 1)} Ranged-{"Yes" if weapon.is_ranged else "No"}')
            index += 1

    @staticmethod
    def player_armors(armors: list):
        index: int = 0
        for armor in armors:
            print(f'ID-{index:02} | {armor.name}: Def-{armor.defense} AC-{armor.AC}\n'
                  f'      | {" " * (len(armor.name) + 1)} Dur-{armor.durability}/{armor.durability_max} Res-{", ".join(armor.resistances)}'
                  )
            index += 1

    @staticmethod
    def shop():
        pass

    class Actions:

        @staticmethod
        def menu_help():
            print('Help: (h)elp, (s)tatus, sho(p), (r)epair, hunt (e)nemy, hea(l), pass(z)')

        @staticmethod
        def status():
            print(GameState.player_actor)

        @staticmethod
        def attack():
            GameState.player_actor.attack()

        # @staticmethod
        # def hunt_enemy():  # Mega broken bc Circular dependency
            # Events.generate_enemy()

        @staticmethod
        def repair():
            GameState.player_actor.repair()

        @staticmethod
        def heal():
            GameState.player_actor.heal()

        @staticmethod
        def shop():
            GameState.player_actor.shop()

        combat_actions: dict = {
            'help': lambda: Menu.Actions.menu_help(),
            'h': lambda: Menu.Actions.menu_help(),
            'attack': lambda: Menu.Actions.attack(),
            'a': lambda: Menu.Actions.attack(),
            'pass': lambda: 0,
            'z': lambda: 0,
            'status': lambda: Menu.Actions.status(),
            's': lambda: Menu.Actions.status(),
            'hunt enemy': lambda: 0,  # Menu.Actions.hunt_enemy(),
            'e': lambda: 0,  # Menu.Actions.hunt_enemy()
        }
        noncombat_actions: dict = {
            'help': lambda: Menu.Actions.menu_help(),
            'h': lambda: Menu.Actions.menu_help(),
            'status': lambda: Menu.Actions.status(),
            's': lambda: Menu.Actions.status(),
            'shop': '',
            'p': '',
            'repair': lambda: Menu.Actions.repair(),
            'r': lambda: Menu.Actions.repair(),
            'hunt enemy': lambda: 0,  # Menu.Actions.hunt_enemy(),
            'e': lambda: 0,  # Menu.Actions.hunt_enemy(),
            'heal': lambda: Menu.Actions.heal(),
            'l': lambda: Menu.Actions.heal()
        }
        nonfree_actions: list = [
            'attack',
            'a',
            'hunt enemy',
            'e',
            'repair',
            'r',
            'heal',
            'l',
            'pass',
            'z'
        ]
