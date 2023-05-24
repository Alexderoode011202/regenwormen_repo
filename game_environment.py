"""
This file will contain the classes and keep track of the game, whose turn it is and how has what amount of points
"""
import random
from needed_classes import Tile, Player, Dice, Stop_Move, Information_State

from typing import Union, Dict, List, Optional


class IllegalMoveError(Exception):
    def __init__(self):
        super().__Init__()


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

            subsets[result] = {"eyes_per_die": result,
                               "total_value": total_value,
                               "worm_presence": worm_presence,
                               "frequency": frequency}

    return subsets


def validity_dice_check(used_values: dict) -> int:
    """
    Eliminates the dice which cannot be used anymore
    :param dice_results: contains a list of results from the dice
    :param used_values: contains the subset dictionary the player carries
    :returns: possibly filtered version of dice_results
    """

    amount_used_dice: int = 0
    # print(f"USED VALUES: {used_values}")
    for frequency in used_values["frequency"]:
        amount_used_dice += frequency

    return amount_used_dice


class Gamestate:
    def __init__(self, players: Dict[str, Optional[Player]] = ["player 1", "player 2", "player 3", "player 4"]) -> None:
        ## Part 1
        # General info:
        self.available_tiles: List = []
        self.points_list: range = range(21, 37)
        self.dice_amount: int = 8
        player_names:  Dict[str, Optional[Player]] = players
        self.full_dice_list: List[Dice]
        self.players: list
        self.leader: Player
        self.winner = None

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
        for name in tuple(players.keys()):
            if not players[name]:
                # for human players
                self.players.append(Player(name=name))
            else:
                # for bot
                self.players.append(players[name])

        self.leader = random.choice(self.players)

    def get_leading_player(self):
        return self.leader

    def assign_new_leader(self):
        try:
            self.leader = self.players[self.players.index(self.leader) + 1]
        except IndexError:
            self.leader = self.players[0]

        # reset temporary info
        self.leader.points = 0
        self.leader.subsets = {"eyes_per_die": [],
                              "frequency": [],
                              }

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
            # eyes_per_die & frequency
            player_subsets: dict = leading_player.get_subset()
            played_dice: int = validity_dice_check(player_subsets)
            try:
                # print(f"last move was: {player_move.get_type()}")
                # print(f"want to roll again:{player_move.check_roll_again()}")
                if player_move.get_type() == "subset move":
                    if not player_move.check_roll_again():
                        # print("KEEP DICE RESULTS")
                        dice_results = dice_results
                    else:
                        # print("DONT KEEP DICE RESULTS")
                        dice_results = self.roll_dice(subset=8 - played_dice)
            except:
                dice_results: List[Union[int, str]] = self.roll_dice(subset=8 - played_dice)

            # make all subsets:
            # 'worm': eyes_per_die, frequency, etc.
            all_subsets: dict = create_subsets(dice_results)

            # filter out all illegal subsets
            filtered_subsets: dict = dict()
            for subset in all_subsets:
                if not (subset in player_subsets["eyes_per_die"]):
                    filtered_subsets[subset] = all_subsets[subset]
                else:
                    continue

            # dont let player play in case of no possible subsets and player rolled dice again:
            try:
                if filtered_subsets == dict() and player_move.check_roll_again():
                    # print(f"{leading_player} CANNOT MAKE A MOVE DUE TO LACK OF SUBSETS")
                    player_move = Stop_Move()
                else:
                    # let player make move:
                    player_move = leading_player.make_move(subset=filtered_subsets,
                                                           dice_results=dice_results,
                                                           info_state=Information_State(players=self.players,
                                                                                        tiles_on_table=self.available_tiles))
            except:
                player_move = leading_player.make_move(subset=filtered_subsets, dice_results=dice_results,
                                                       info_state=Information_State(players=self.players,
                                                                                    tiles_on_table=self.available_tiles))

            # process player move:
            if player_move.get_type() != "subset move" and player_move.get_type() != "error move":
                leader_stops = True

                # if tile move:
                if player_move.get_type() == "tile move":
                    # print("REACHED")
                    # move tile to player:
                    # from player
                    if player_move.get_origin() is not None:
                        leading_player.add_tile(player_move.get_origin().take_tile())

                    # from table
                    else:
                        leading_player.add_tile(self.give_tile(player_move.get_tile()))
                # If player gives up
                else:
                    self.remove_tile_from_table()
                    if not self.available_tiles:
                        winner = self.get_winner()


            # if subset move:
            else:
                if player_move.get_type() == "subset move":
                    leading_player.add_subset(player_move.get_current_subsets())
                    # print(f"previously chosen: {leading_player.get_subset()['eyes_per_die']}")
                else:
                    print("TRY AGAIN")

                    # switch to new player:
                    # POSSIBLE
        # self.assign_new_leader()
        print("ROUND HAS ENDED")

    def remove_tile_from_table(self) -> None:
        self.available_tiles.pop()

    def test_func(self):
        print("TEST TEST TEST")


    def calculate_winner(self):
        scoreboard: dict = dict()
        for player in self.players:
            print(f"player: {player}, worms: {player.worms}")
            scoreboard[player] = player.worms

        print("----------------")
        print(self.players)
        print(scoreboard)
        print("----------------")
        highest_score: int = 0
        winner: Optional[Player] = None
        for player in scoreboard:
            if scoreboard[player] > highest_score:
                print(f"high_score: {highest_score}, own score: {scoreboard[player]}")
                winner = player
                highest_score = scoreboard[player]

        # announce winner:
        print(f"The winner is: {winner} with {highest_score} worms!")
        self.winner = winner

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

    def get_winner(self) -> Optional[Player]:
        return self.winner

    """
    def calculate_winner(self) -> Player:
        winner = None
        max_worms = 0
        for player in self.players:
            if player.worms > max_worms:
                winner = player
                max_worms = player.worms
            else:
                continue

        self.winner = winner
    """

    def give_tile(self, tile: Tile) -> Tile:
        return self.available_tiles.pop(self.available_tiles.index(tile))



