###################################
# Imports                         #
###################################


import random as rand

from TextGame.GameState import GameState
from TextGame.GameObject import GameObject


###################################
# Code Execution                  #
###################################


rand.seed()


def run_game() -> None:
    GameObject.start_game()
    while GameState.is_active_game:
        GameObject.round()


user_continue = "y"
while user_continue == "y":
    run_game()
    user_continue = input("Continue? [Y/n]").lower()



