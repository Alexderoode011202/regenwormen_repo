"""
This file will contain all the code necessary to play a game of Regenwormen.
It will set up the entire game environment, and allow bots to play and test in the given environment.
"""
from typing import Union
import random


class Dice:
    def __init__(self):
        self.sides: tuple = (1, 2, 3, 4, 5, "worm")

    def roll(self) -> Union[int, str]:
        return random.choice(self.sides)


class Tile:
    def __init__(self, points: int, worms: int):
        self.points = points
        self.worms = worms

    def get_points(self) -> int:
        return self.points

    def get_worms(self) -> int:
        return self.worms

    def __str__(self) -> str:
        return f"Tile(points: {self.points}, worms: {self.worms})"


class Player:
    def __init__(self, name: str):
        self.name = name
        self.points = 0
        self.worms = 0
        self.owned_tiles = []
        self.subsets = dict()

    def get_tile(self, tile: Tile) -> None:
        """Gives the player a tile"""
        self.owned_tiles.append(tile)

    def check_top_tile(self) -> Tile:
        return self.owned_tiles[-1]

    def take_tile(self):
        return self.owned_tiles.pop()

    def add_tile(self, tile: Tile):
        self.owned_tiles.append(tile)


    def make_move(self, subset: dict) -> Union["Stop_Move", "Tile_Move"]:
        """
        Allows player to make a move.
        The player can make three types of choice
        """

        pass

    def get_subsets(self):
        return self.subsets


class Move:
    def __init__(self, move_type: str):
        self.type = move_type

    def get_type(self) -> str:
        return self.type


class Tile_Move(Move):
    def __init__(self, tile: Tile, player: Player = None):
        super().__init__(move_type="tile move")
        self.tile = tile
        self.from_player = player

    def get_origin(self) -> Union[Player, None]:
        return self.from_player

    def get_tile(self) -> Tile:
        return self.tile


class Stop_Move(Move):
    def __init__(self):
        super().__init__(move_type="stop")


"""
some_die: Dice = Dice()
print(some_die.roll())
"""