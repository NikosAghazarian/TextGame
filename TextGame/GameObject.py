from TextGame.GameState import GameState
from TextGame.Events import Events
from TextGame.ActorUnit import ActorUnit
from TextGame.Menu import Menu
from TextGame.Weapon import Weapon


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
        GameState.turn_count = 0
        GameState.actors = []
        GameState.is_active_game = True
        GameState.nonfree_action_taken = False
        GameState.enemy_count = 0
        GameState.merchant_present = False

        # Player Init.
        weapon: Weapon = Weapon('Sword-like Catfish', 6, 2, 1, damage_type='Slicing')
        GameState.player_actor = ActorUnit(name=player_name, health=2**20, starter_weapon=weapon, hostility=0)
        GameState.player_actor.weapons.append(Weapon('Fists'))
        GameState.actors.append(GameState.player_actor)

        Events.generate_enemy()

    @staticmethod
    def turn() -> None:
        """
        Takes turns sequentially for each actor.

        TODO: Consider creating turn method on ActorUnit to move all Menu dependency off of GameObject.
        """
        print('\n-------------------------------------')
        if GameState.player_actor.health < 1:  # Loss Condition
            print('Game Over')
            GameState.is_active_game = False
            return
        for actor in GameState.actors:
            if actor is GameState.player_actor:
                Menu.menu_logic()
            else:  # actions to occur on every enemy turn
                if GameState.nonfree_action_taken:
                    GameState.turn_count += 1
                    actor.attack(target=GameState.player_actor)
                    Events.random_event()
        GameState.nonfree_action_taken = False

    @staticmethod
    def reset() -> None:
        """
        Alias for GameObject.start_game().
        """
        GameObject.start_game()



