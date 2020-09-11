from TextGame.GameState import GameState
from TextGame.Weapon import Weapon


class Menu:
    """
    Namespace class
    """

    @staticmethod
    def menu_logic() -> None:
        """ """
        while True:
            user_command = input('Give your command: ').lower()

            if user_command in Menu.Actions.nonfree_actions:  # Enemies only attack if player acts.
                GameState.nonfree_action_taken = True

            if GameState.enemy_count != 0 and user_command in Menu.Actions.combat_actions:  # Combat Menu.
                Menu.Actions.combat_actions[user_command]()
                break
            elif user_command in Menu.Actions.noncombat_actions:  # Non-combat Menu.
                Menu.Actions.noncombat_actions[user_command]()
                break
            else:
                print('Invalid command.')
                continue

    @staticmethod
    def targeting() -> int:
        """ """
        index: int = 0
        banned_index: list = [0]
        for actor in GameState.actors:
            if (actor is not GameState.player_actor) and actor.hostility > 255:
                print(f'ID-{index:02} | {actor.name}: HP-{actor.health} Def-{actor.armor.defense}\n'
                      f'      | {" " * (len(actor.name) + 1)} AC-{actor.armor.AC} Res-{", ".join(actor.armor.resistances)}')
            else:
                banned_index.append(index)
            index += 1
        return banned_index

    @staticmethod
    def player_weapons() -> None:
        """ """
        index: int = 0
        for weapon in GameState.player_actor.weapons:
            print(f'ID-{index:02} | {weapon.name}: Dmg-{weapon.dmg} Type-{weapon.dmg_type}\n'
                  f'      | {" " * (len(weapon.name) + 1)} Hit-+{weapon.hit_mod} Dur-{weapon.durability}/{weapon.durability_max}\n'
                  f'      | {" " * (len(weapon.name) + 1)} Ranged-{"Yes" if weapon.is_ranged else "No"}')
            index += 1

    @staticmethod
    def player_armors(armors: list) -> None:
        """ """
        index: int = 0
        for armor in armors:
            print(f'ID-{index:02} | {armor.name}: Def-{armor.defense} AC-{armor.AC}\n'
                  f'      | {" " * (len(armor.name) + 1)} Dur-{armor.durability}/{armor.durability_max} Res-{", ".join(armor.resistances)}'
                  )
            index += 1

    @staticmethod
    def shop() -> None:
        """ """
        index: int = 0
        for item in GameState.shop_inventory:
            print(f'###########\n#   {index:03d}   #\n###########\n{item}')
            index += 1

    @staticmethod
    def buy() -> None:
        Menu.shop()
        choice_idx = int(input(f'Which item do you want to buy? [0 - {len(GameState.shop_inventory)-1}]'))
        if 0 <= choice_idx < len(GameState.shop_inventory):
            chosen_item = GameState.shop_inventory.stored_items[choice_idx]
            try:
                GameState.player_actor.inventory.gold -= chosen_item.value
                if isinstance(chosen_item, Weapon):
                    GameState.player_actor.weapons.append(chosen_item)
                else:
                    GameState.player_actor.inventory.store(chosen_item)
                GameState.shop_inventory.remove_item(chosen_item.name)
            except ValueError:
                print('Not enough gold!')

    class Actions:
        """ """

        @staticmethod
        def menu_help() -> None:
            """ """
            print('Help: (h)elp, (s)tatus, sho(p), (r)epair, hea(l), pass(z)')

        @staticmethod
        def status() -> None:
            """ """
            print(GameState.player_actor)

        @staticmethod
        def attack() -> None:
            """ """
            GameState.player_actor.attack()

        @staticmethod
        def repair() -> None:
            """ """
            GameState.player_actor.repair()

        @staticmethod
        def heal() -> None:
            """ """
            GameState.player_actor.heal()

        @staticmethod
        def show_inventory() -> None:
            print(GameState.player_actor.inventory)

        combat_actions: dict = {
            'help': lambda: Menu.Actions.menu_help(),
            'h': lambda: Menu.Actions.menu_help(),
            'attack': lambda: Menu.Actions.attack(),
            'a': lambda: Menu.Actions.attack(),
            'pass': lambda: 0,
            'z': lambda: 0,
            'status': lambda: Menu.Actions.status(),
            's': lambda: Menu.Actions.status(),
            'repair': lambda: Menu.Actions.repair(),
            'r': lambda: Menu.Actions.repair()
        }
        noncombat_actions: dict = {
            'help': lambda: Menu.Actions.menu_help(),
            'h': lambda: Menu.Actions.menu_help(),
            'status': lambda: Menu.Actions.status(),
            's': lambda: Menu.Actions.status(),
            'shop': lambda: Menu.shop(),
            'p': lambda: Menu.shop(),
            'repair': lambda: Menu.Actions.repair(),
            'r': lambda: Menu.Actions.repair(),
            'heal': lambda: Menu.Actions.heal(),
            'l': lambda: Menu.Actions.heal(),
            'inventory': lambda: Menu.Actions.show_inventory(),
            'i': lambda: Menu.Actions.show_inventory(),
            'buy': lambda: Menu.buy(),
            'b':lambda: Menu.buy()
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
