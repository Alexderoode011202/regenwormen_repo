"""
This file will contain the classes and keep track of the game, whose turn it is and how has what amount of points
"""
from typing import List
from needed_classes import Tile, Player, Dice

# General info:
points_list: range = range(21, 37)
dice_amount: int = 8

class Gamestate:
    def __init__(self, players: List[str]) -> None:
        self.available_tiles: List = []

        # make all the tiles:
        for points in points_list:
            worms: int
            if points <=24:
                worms = 1
            elif points <=28:
                worms = 2
            elif points <= 32:
                worms = 3
            else:
                worms = 4
            self.available_tiles.append(Tile(points=points, worms=worms))

        # make the dice:
        full_dice_list: List[Dice] = []
        for num in range(1, dice_amount + 1):
            full_dice_list.append(Dice())

        # Instantiate the players:





