class GameState:
    """
    Namespace class that manages game-global attributes.

    :damage_types: ``List[str]`` - Types of damage available for weapon damage and armor resistance.
    :actors: ``List[ActorUnit]`` - List of active entities in the game.
    :round_count: ``int`` - Combat turns taken.
    :player_actor: ``ActorUnit`` - Reference to the ``ActorUnit`` representing the player.
    :is_active_game: ``bool`` - Flag variable. Determined at start of turn cycle if player HP==0.
    :nonfree_action_taken: ``Bool`` - Flag variable. Used to determine whether hostile entities get to act.
    :enemy_count: ``int`` - Counts the number of active enemy combatants for the purpose of determining whether player is in combat.
    :merchant: ``ActorUnit|None`` - Reference to the ``ActorUnit`` representing the current shop. Is ``None`` if there is no shop present.
    """

    damage_types: list = ['Slicing', 'Piercing', 'Bludgeoning', 'Fire', 'Cold', 'Mental']
    equip_tiers: list = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Mythic']
    actors: list = []
    round_count: int = 0
    player_actor: 'ActorUnit' = None
    merchant_actor: 'ActorUnit' = None
    is_active_game: bool = True
    nonfree_action_taken: bool = False
    enemy_count: int = 0
