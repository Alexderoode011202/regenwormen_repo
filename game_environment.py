"""
This file will contain the classes and keep track of the game, whose turn it is and how has what amount of points
"""

from needed_classes import Tile, Player, Dice
import random
from typing import Union, Dict, List


def create_subsets(results) -> Dict[Union[int, str], Dict[str, Union[int, bool]]]:
    """
    Creates the subsets based on what was thrown.
    The subsets get returned in the form of a nested dictionary.
    The keys of the main dictionary are the values that a die can give.
    the values of the main dictionary contain which contain the total_value and word_presence
    """
    subsets: dict = dict()
    for result in results:
        if result not in list(subsets.keys()):
            frequency: int = results.count(result)
            total_value: int
            worm_presence: bool = False
            try:
                total_value = int(frequency * result)
            except ValueError:
                # In case of worms
                total_value = frequency * 5

            if result == "worm":
                worm_presence = True

            subsets[result] = {"total_value": total_value, "worm_presence": worm_presence}

    return subsets


class Gamestate:
    def __init__(self, players: List[str] = ["player 1", "player 2", "player 3", "player 4"]) -> None:
        ## Part 1
        # General info:
        self.available_tiles: List = []
        self.points_list: range = range(21, 37)
        self.dice_amount: int = 8
        player_names: list[str] = players
        self.full_dice_list: List[Dice]
        self.players: list
        self.leader: Player

        # make all the tiles:
        for points in self.points_list:
            worms: int
            if points <= 24:
                worms = 1
            elif points <= 28:
                worms = 2
            elif points <= 32:
                worms = 3
            else:
                worms = 4
            self.available_tiles.append(Tile(points=points, worms=worms))

        # make the dice:
        self.full_dice_list = []
        for num in range(1, self.dice_amount + 1):
            self.full_dice_list.append(Dice())

        # Instantiate the players:
        self.players = []
        for name in player_names:
            self.players.append(Player(name=name))

        self.leader = random.choice(self.players)

    def get_leading_player(self):
        return self.leader

    def assign_new_leader(self):
        try:
            self.leader = self.players[self.players.index(self.leader) + 1]
        except IndexError:
            self.leader = self.players[0]

    def play_round(self) -> None:
        leading_player: Player = self.get_leading_player()
        leading_player.make_move()
        self.assign_new_leader()

    def get_dice(self) -> List[Dice]:
        return self.full_dice_list.copy()

    def roll_dice(self, subset: int = 8) -> List[Union[int, str]]:
        results: List[Union[int, str]] = []
        dice_set: List[Dice] = self.get_dice()[:subset]
        for die in dice_set:
            results.append(die.roll())
        return results

    def check_validity(self, current_results: dict[Union[str, int], int]):
        """
        Checks the validity of the moves a player could make
        and filters out the illegal ones
        """

        pass


