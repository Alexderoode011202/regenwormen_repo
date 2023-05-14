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
        self.subsets: dict = {"eyes_per_die": [],
                              "frequency": [],
                              }


    def __str__(self) -> str:
        return f"{self.name} with {self.worms} worms with {self.check_top_tile()} as top tile"

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

    def make_move(self, subset: dict, dice_results, info_state: "Information_State") -> Union["Stop_Move", "Tile_Move", "Subset_Move"]:
        """
        Allows player to make a move.
        The player can make three types of choice.
        This method is optimized for human use

        :param subset: contains all the subsets one can make
        :param dice_results: is a list containing the dice results.
        :param info_state": is an Information_State object
        containing all the info needed to gather information
        and make informed decisions
        :returns: something like a Move object containing the player's decision
        """
        no_choice: bool = False
        if subset == dict():
            no_choice = True

        ## get all the information needed
        # Show what has been thrown
        string_format: str = ""
        for num, value in enumerate(dice_results):
            if num == 0:
                string_format = str(value)
            else:
                string_format += f", {value}"
        print(f"DICE RESULTS: {string_format}")

        # show player's current score:
        print(f"Own score is: {self.points} points.")

        # show what tiles are available in what way
        for player in info_state.get_all_players():
            if player == self:
                continue
            else:
                # print(f"{player} has: {player.check_top_tile()}")
                continue
        for tile in info_state.get_tiles_on_table():
            print(f"The table has: {tile}")

        # Show other players and their tiles
        print("Players:")
        players_and_tiles: dict = info_state.get_stealable_tiles()
        for player in players_and_tiles:
            print(f"-{player} with {players_and_tiles[player]}")

        # portray all possibilities
        if not no_choice:
            for num, possibility in enumerate(subset):
                print(f"[{num + 1}] eye: {possibility}, ")
                print(f"total value: {subset[possibility]['total_value']}, ")
                print(f"worm presence: {subset[possibility]['worm_presence']}, ")
                print(f"frequency: {subset[possibility]['frequency']}")
                print('---------')
        else:
            print("YOU CANNOT CHOOSE ANY SUBSETS")

        # show your options:
        choice: str = ""
        if not no_choice:
            while choice != "1" and choice != "2" and choice != "3":
                print(f"choice: {choice}")
                print("give a number to make your choice")
                print("[1] choose a subset and keep playing")
                print("[2] Take a tile from the table or from another player")
                choice = input("[3] Give up\n")

        else:
            while choice != "2" and choice != "3":
                print(f"choice: {choice}")
                print("give a number to make your choice")
                print("[2] Take a tile from the table or from another player")
                choice = input("[3] Give up\n")



        if choice == "1":
            # If deciding to keep playing
            # let player choose subset
            subset_choice = input("choose the value of eyes per die you wish to keep\n")

            # process player choice
            try:
                subset_choice = int(subset_choice)
            except:
                subset_choice = "worm"

            chosen_subsets = subset[subset_choice]
            return Subset_Move(chosen_subset=chosen_subsets)

        elif choice == "2":
            # if choosing to take a tile instead
            # Choose value of tile you want:
            tile_value: int = int(input("What is the point value of the tile you want?:\n"))

            # check whether tile is from table:
            for tile in info_state.get_tiles_on_table():
                if tile.get_points() == tile_value:
                    # return if that's the case
                    if self.points >= tile.get_points():
                        return Tile_Move(tile=tile, player=None)
                    else:
                        print(f"TILE CANNOT BE CHOSEN: YOU HAVE: {self.points} POINTS. TILE POINT VALUE IS: {tile.get_points()}")

            # check whether tile is stealable
            for player in info_state.get_stealable_tiles():
                if info_state.get_stealable_tiles()[player].get_points() == self.points:
                    return Tile_Move(tile=info_state.get_stealable_tiles()[player], player=player)

        else:
            # if choosing to give up
            return Stop_Move()

    def get_subset(self):
        return self.subsets

    def add_subset(self, subset:  Dict[Union[str, int], Dict[str, int]]) -> None:
        frequency: int
        eyes: Union[int, str]
        for key in subset:
            try:
                old_values: list = self.subsets[key]
                old_values.append(subset[key])
                if key == "eyes_per_die":
                    eyes = subset[key]
                    if eyes == "worm":
                        eyes = 5
                elif key == "frequency":
                    frequency = subset[key]

            except KeyError:
                continue

        self.points += (frequency * eyes)
        return None


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


class Subset_Move(Move):
    def __init__(self, chosen_subset: Dict[Union[str, int], Dict[str, int]]) -> None:
        super().__init__(move_type="subset move")
        self.subsets = chosen_subset

    def get_current_subsets(self) -> Dict[Union[str, int], Dict[str, int]]:
        return self.subsets


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
