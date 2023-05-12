"""
This file will contain all the code necessary to play a game of Regenwormen.
It will set up the entire game environment, and allow bots to play and test in the given environment.
"""
from typing import Union, Iterable, Tuple, List, Optional, Dict
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

    def check_top_tile(self) -> Optional[Tile]:
        try:
            top_tile = self.owned_tiles[-1]
        except IndexError:
            top_tile = None
        return top_tile

    def take_tile(self):
        return self.owned_tiles.pop()

    def add_tile(self, tile: Tile):
        self.owned_tiles.append(tile)

    def make_move(self, subset: dict, dice_results, info_state: "Information_State") -> Union["Stop_Move", "Tile_Move"]:
        """
        Allows player to make a move.
        The player can make three types of choice.
        This method is optimized for human use
        """

        ## get all the information needed
        # Show what has been thrown
        string_format: str = ""
        for num, value in enumerate(dice_results):
            if num == 0:
                string_format = str(value)
            else:
                string_format += f", {value}"
        print(string_format)
        print("\n")
        # Show other players and their tiles
        print("Players:")
        players_and_tiles: dict = info_state.get_stealable_tiles()
        for player in players_and_tiles:
            print(f"-{player} with {players_and_tiles[player]}")
        print("\n")

        # show your options:
        choice: str = ""
        while choice != "1" or "2" or "3":
            print("give a number to make your choice")
            print("[1] choose a subset and keep playing")
            print("[2] Take a tile from the table or from another player")
            choice = input("[3] Give up\n")

        if choice == "1":
            # If deciding to keep playing
            subset_choice: str = ""
            while subset_choice not in list(subset.keys()):
                for num, possibility in enumerate(subset, start=1):
                    print(f"[{num}] eye: {possibility}, "
                          f"total value: {possibility['total_value']}, "
                          f"worm presence: {possibility['worm_presence']}, "
                          f"frequency: {possibility['frequency']}")

                subset_choice = input("choose the value of eyes per die you wish to keep")

        elif choice == "2":
            # if choosing to take a tile instead
            pass

        else:
            # if choosing to give up
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


class Information_State:
    def __init__(self, players: Iterable[Player], tiles_on_table: Iterable[Tile]):
        self.players = players
        self.tiles_on_table = tiles_on_table

    def get_all_players(self) -> Tuple[Player]:
        return tuple(self.players)

    def get_tiles_on_table(self) -> List[Tile]:
        return list(self.tiles_on_table)

    def get_stealable_tiles(self) -> Dict[Player, Optional[Tile]]:
        player_tile_dict: dict = dict()
        for player in self.get_all_players():
            player_tile_dict[player] = player.check_top_tile()
        return player_tile_dict



"""
some_die: Dice = Dice()
print(some_die.roll())
"""