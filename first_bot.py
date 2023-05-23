from needed_classes import Player, Tile, Tile_Move, Stop_Move, Subset_Move, Error_Move
from game_environment import Gamestate, Information_State
from typing import Dict, List, Tuple, Optional, Union
from random import sample, choice


class Random_Bot(Player):
    def __init__(self):
        super().__init__(name="Mr. Random Bot")

    def __str__(self):
        return "Random bot"

    def make_move(self, subset: dict, dice_results, info_state: "Information_State",
                  old_move: Optional["Subset_Move"] = None) -> Union[
        "Stop_Move", "Tile_Move", "Subset_Move", "Error_Move"]:
        """
        This bot makes random

        strategy:
        1. always try to pick a subset until <3 dice are left
            1A. The chosen subset must be worms if possible, otherwise take a random subset

        2. If no <3 dice left AND already have worms, randomly pick a tile the bot can take. OTHERWISE keep playing

        3. if another subset is not possible and the value chosen doesn't allow to pick another tile, give up
        """
        ## IMPORTANT INFO
        own_points: int = self.points
        tiles_on_table: List[Tile] = info_state.get_tiles_on_table()
        stealable_tiles: Dict[Player, Optional[Tile]] = info_state.get_stealable_tiles()

        # check worms:
        chose_worms: bool = False
        for thrown_value in self.get_subset()["eyes_per_die"]:
            if thrown_value == "worm":
                chose_worms = True

        # check dice left:
        dice_left: int = len(dice_results)

        # formalize player move:
        player_move: Union[Subset_Move, Error_Move, Stop_Move, Tile_Move] = None

        # check what tiles can be taken:
        takeable_tiles: List[Tile] = tiles_on_table.copy()
        for tile in tuple(stealable_tiles.values()):
            if tile is not None:
                takeable_tiles.append(tile)

        ## MAKE DECISIONS
        # if <3 dice left and already have worms:
        if chose_worms and dice_left < 3:
            victim_tile: Optional[Tile] = None
            # check whether there are any Tiles that can be taken
            for tile in takeable_tiles:
                if tile.get_points() == own_points:

                    # if tile on table
                    if tile in tiles_on_table:
                        player_move = Tile_Move(tile=tile, player=None)

                    # if tile belongs to player
                    else:
                        for player in stealable_tiles:
                            try:
                                if stealable_tiles[player].get_points() == own_points:
                                    player_move = Tile_Move(tile=stealable_tiles[player], player=player)
                            except:
                                continue
        # if no worms:
        elif not chose_worms:
            # 1. go get another subset and throw again
            for key in subset:
                if key == "worm":
                    player_move = Subset_Move(chosen_subset=subset[key], roll_again=True)

            # 2. if no worm subset possible
            if player_move is None:
                if subset != dict():
                    if dice_left < 3:
                        player_move = Subset_Move(chosen_subset=subset[choice(tuple(subset.keys()))],
                                                  roll_again=False)
                    else:
                        player_move = Subset_Move(chosen_subset=subset[choice(tuple(subset.keys()))],
                                                  roll_again=True)

                # 3. give up
                else:
                    player_move = Stop_Move()

        # if worms but >=3 dice
        else:
            # choose a new subset
            player_move = Subset_Move(chosen_subset=subset[choice(tuple(subset.keys()))], roll_again=True)

        return player_move
