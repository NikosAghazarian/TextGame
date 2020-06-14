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

GameObject.start_game()

while True:
    GameObject.turn()
    if not GameState.is_active_game:
        user_continue = input("Continue? [Y/n]").lower()
        if user_continue == "y":
            GameObject.reset()
        elif user_continue == "n":
            break
        else:
            continue


