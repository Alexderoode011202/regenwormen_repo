"""
This file is supposed to be executed when wanting to run the regenwormen program
"""
from typing import Dict, List, Union, Optional
from game_environment import create_subsets, Gamestate
from needed_classes import Player, Dice, Tile


def play_game(players: Dict[str, Optional[Player]]) -> None:
    """
    when giving the players give them in the form of a dictionary.
    The key must be the name of the player
    The value must be the bot object if the player is a bot.
    Otherwise, leave it as None.
    """
    # formalize the gamestate
    state: Gamestate = Gamestate(players=players)

    state.play_round()


play_game({"test subject 1": None, "test subject 2": None})