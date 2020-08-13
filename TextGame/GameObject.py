from TextGame.GameState import GameState
from TextGame.Events import Events
from TextGame.Weapon import Weapon
from TextGame.UnitTypes import Player


class GameObject:
    """
    Namespace class that manages game-global methods.
    """

    @staticmethod
    def start_game() -> None:
        """
        Static method for initializing the game state.
        """

        player_name = input('What is your name? ')
        GameState.round_count = 0
        GameState.actors = []
        GameState.is_active_game = True
        GameState.nonfree_action_taken = False
        GameState.enemy_count = 0
        GameState.merchant_present = False

        # Player Init.
        weapon: Weapon = Weapon('Sword-like Catfish', 200, 999, 1, damage_type='Slicing')
        GameState.player_actor = Player(name=player_name, health=2**20, starter_weapon=weapon)
        GameState.player_actor.weapons.append(Weapon('Fists'))
        GameState.player_actor.isPlayer = True
        GameState.actors.append(GameState.player_actor)
        print(GameState.player_actor)

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

    @staticmethod
    def reset() -> None:
        """
        Alias for GameObject.start_game().
        """
        GameObject.start_game()
