from TextGame.GameState import GameState
from TextGame.Events import Events
from TextGame.Weapon import Weapon
from TextGame.Armor import Armor
from TextGame.UnitTypes import Player
from TextGame.Inventory import Inventory
from TextGame.Item import Item


class GameObject:
    """
    Namespace class that manages game-global methods.
    """

    @staticmethod
    def start_game() -> None:
        """
        Static method for initializing the game state.
        """

        GameState.round_count = 0
        GameState.actors = []
        GameState.is_active_game = True
        GameState.nonfree_action_taken = False
        GameState.enemy_count = 0
        GameState.merchant_present = False

        # Player Init.
        player_name = input('What is your name? ')
        starter_weapon: Weapon = Weapon('Sword-like Catfish', 200, 999, 1, damage_type='Slicing')
        GameState.player_actor = Player(player_name, 2**20, starter_weapon)
        GameState.player_actor.weapons.append(Weapon('Fists'))
        GameState.player_actor.isPlayer = True
        GameState.player_actor.inventory.gold = 10000
        for i in range(3):  # Start with 3 health pots
            GameState.player_actor.inventory.store(Item.gen_health_potion())
        GameState.actors.append(GameState.player_actor)
        print(GameState.player_actor)

        # Shop Init
        shop = Inventory()
        shop.gold = 200
        for i in range(3):  # Start with 3 health pots, weapons, and armors
            shop.store(Item.gen_health_potion())
            shop.store(Weapon.gen_weapon(1))
            shop.store(Armor.gen_armor(1))
        GameState.shop_inventory = shop

        Events.generate_enemy()

    @staticmethod
    def round() -> None:
        """
        Takes turns sequentially for each actor.
        """

        print('\n-------------------------------------')

        if GameState.player_actor.health < 1:  # Loss Condition
            print('Game Over')
            GameState.is_active_game = False
            return

        for actor in GameState.actors:
            actor.turn()

        if GameState.nonfree_action_taken:
            GameState.round_count += 1
            Events.random_event()

        GameState.nonfree_action_taken = False
