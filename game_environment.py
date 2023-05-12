"""
This file will contain the classes and keep track of the game, whose turn it is and how has what amount of points
"""

from needed_classes import Tile, Player, Dice, Tile_Move, Stop_Move, Information_State
import random
from typing import Union, Dict, List, Iterable, Tuple


def create_subsets(results: list) -> Dict[Union[int, str], Dict[str, Union[int, bool]]]:
    """
    Creates the subsets based on what was thrown.
    The subsets get returned in the form of a nested dictionary.
    The keys of the main dictionary are the values that a die can give.
    the values of the main dictionary contain which contain the total_value, word_presence, and frequency
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

            subsets[result] = {"total_value": total_value,
                               "worm_presence": worm_presence,
                               "frequency": frequency}

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
        """
        Checks which player can play.
        After rolling dice the player can choose to:
        1. keep rolling dice
        2. take a tile from table/player
        3. stop/lose tile
        """

        # get leading player and his status
        leading_player: Player = self.get_leading_player()
        leader_stops: bool = False

        while not leader_stops:
            # check how many dice he has
            player_subsets: dict = leading_player.get_subsets()
            played_dice: int = 0

            try:
                for subset in player_subsets:
                    played_dice += subset["frequency"]

            except KeyError:
                played_dice = 0

            # roll the dice
            dice_results: List[str, int] = self.roll_dice(subset=8 - played_dice)

            # filter out illegal moves/dice
            # maybe replace lower bit of code with function some day
            try:
                for subset in player_subsets.keys():
                    for _ in range(dice_results.count(subset)):
                        dice_results.remove(subset)
            except KeyError:
                subset = subset

            # form all the possible subsets
            possible_subsets: dict = create_subsets(results=dice_results)

            # let player choose action/subset
            player_action: Union[Tile_Move, Stop_Move] = leading_player.make_move(subset=possible_subsets,
                                                                                  dice_results=dice_results, info_state=Information_State(players=self.players, tiles_on_table=self.available_tiles))

            # check whether player is done
            if player_action.get_type() == "stop" or "tile move":
                leader_stops = True

                # Deal with tile exchange
                if player_action == "tile move":
                    # collect info
                    victim: Player = player_action.get_origin()

                    # execute tile exchange
                    leading_player.add_tile((victim.take_tile()))
            else:
                continue

    def calculate_winner(self):
        scoreboard: dict = dict()
        for player in self.players:
            scoreboard[player.name] = player.worms

        highest_score: int = 0
        winner: str = ""
        for player, score in tuple(zip(tuple(scoreboard.keys()), tuple(scoreboard.values()))):
            if score > highest_score:
                highest_score = score
                winner = player
            elif (score == highest_score) and (score != 0):
                winner += f" and {player}"

        # announce winner:
        print(f"The winner is: {winner} with {highest_score} worms!")

        # POTENTIALLY RETURN SOMETHING LATER
        return None

    def get_dice(self) -> List[Dice]:
        return self.full_dice_list.copy()

    def roll_dice(self, subset: int = 8) -> List[Union[int, str]]:
        results: List[Union[int, str]] = []
        dice_set: List[Dice] = self.get_dice()[:subset]
        for die in dice_set:
            results.append(die.roll())
        return results



