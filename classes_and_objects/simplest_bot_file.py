from needed_classes import *
from game_environment import *
from typing import List, Dict, Union, Optional

class Simplest_Bot(Player):
    def __init__(self):
        super().__init__(name="Simplest Bot")

    def make_move(self, subset: dict, dice_results, info_state: "Information_State", old_move: Optional["Subset_Move"] = None) -> Union["Stop_Move", "Tile_Move", "Subset_Move", "Error_Move"]:
        """
        attempts to get a tile as quickly as possible with the lowest amount of risk.
        strategy:
        1. check the lowest tile on the table
        2. keep rolling if own points < the lowest tile AND points not in stealable tiles

        :param subset: {n:{"eyes_per_die": n, "total_value": N, ...},
                        x:{"eyes_per_die": n, "total_value": N, ...}
                        ...}
        :param dice_results: [1,3,5,"worm", "worm"]
        :param info_state: Information_State obj.
        :param old_move: None
        :return:
        """



        ## step 0. Acquire all info
        # own info:
        own_points: int = self.points
        got_worms: bool = False
        if "worm" in self.get_subset()["eyes_per_die"]:
            got_worms = True
        # test:
        print(f"BOT POINTS: {self.points}")
        print(f"BOT WORMS: {got_worms}")
        print("---------")
        # state info:
        tiles_on_table: List[Tile] = info_state.get_tiles_on_table()
        tiles_on_table.sort(key=lambda x: x.get_points())
        stealable_tiles: Dict[Player, Optional[Tile]] = info_state.get_stealable_tiles()
        # LIST == []
        lowest_tile: Tile = tiles_on_table[0]
        lowest_value: int = 0
        print(f"LOWEST TILE TEST: {lowest_tile.get_points()}")
        print(f"HIGHEST TILE TEST: {tiles_on_table[-1].get_points()}")
        print("---------")
        if got_worms:
            print("PASSED 1")
            ## step 1. check whether enough points
            if own_points >= lowest_tile.get_points():
                print("PASSED 2")
                ## step 1A. if enough points:
                print("TILE MOVE MADE")
                return Tile_Move(tile=lowest_tile, player=None)

            ## step 2. check whether bot can steal a tile
            for player in stealable_tiles:
                if not stealable_tiles[player]:
                    continue
                else:
                    if stealable_tiles[player].get_points() == own_points:
                        print("TILE MOVE MADE")
                        return Tile_Move(tile=stealable_tiles[player], player=player)

        # step 3. If the bot cannot take a tile in any way, let it throw again
        if subset != dict():
            print("PASSED 3")
            # try to get worms ASAP:
            if "worm" in tuple(subset.keys()):
                print("PASSED 4")
                return Subset_Move(chosen_subset=subset["worm"], roll_again= True)
            else:
                print("PASSED 5")
                chosen_eyes = random.choice(tuple(subset.keys()))
                return Subset_Move(chosen_subset=subset[chosen_eyes], roll_again=True)
        else:
            print("END OF ROUND")
            return Stop_Move()

"""
test = Simplest_Bot()
print(test)
"""
