class GameState:
    """
    Namespace class that manages game-global attributes.
    """

    damage_types: list = ['Slicing', 'Piercing', 'Bludgeoning', 'Fire', 'Cold', 'Mental']
    actors: list = []
    turn_count: int = 0
    player_actor: 'ActorUnit' = None  # Is effectively const after assignment. Reassigned only on reset.
    is_active_game: bool = True
    nonfree_action_taken: bool = False
    enemy_count: int = 0
    merchant_present: bool = False
    merchant: 'Shop' = None
