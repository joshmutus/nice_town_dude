from dataclasses import dataclass
from enum import Enum

class LandType(Enum):
    CLEAR = 0
    GRASS = 1
    TREE = 2
    ROAD = 3
    BUILDING = 4

@dataclass
class CharSheet:
    """Dataclass for holding character sheet attributes."""
    path: str
    columns: int
    count: int

@dataclass
class Buildable:
    """Class for holding things than can be built."""
    name: str
    cost: int
    upkeep: int
    grid_size: tuple[int, int]
    character_sheet: CharSheet

@dataclass
class Town:
    """Class for tracking the economy of the town."""
    population: int
    money: float
    happiness: float
    jank: float
    things: list[Buildable]

house = Buildable(name='house', cost=10, upkeep=10, grid_size=(1,1), character_sheet=CharSheet(path="assets/outdoor/house_small.png", 
                                                                              columns=2, 
                                                                              count=6))
tree = Buildable(name='tree', cost=1, upkeep=0, grid_size=(1,1), character_sheet=CharSheet(path="assets/outdoor/oak_tree.png", 
                                                                          columns=1, 
                                                                          count=1))
fountain = Buildable(name='fountain', cost=20, upkeep=10, grid_size=(1,1), character_sheet=CharSheet(path="assets/outdoor/fountain.png", 
                                                                                    columns=1,
                                                                                    count=1))
hunting_shed = Buildable(name='hunting shed', cost=50, upkeep=5,grid_size=(1,1), character_sheet=CharSheet(path="assets/outdoor/hunting_shed.png", 
                                                                                           columns=1,
                                                                                           count=2))
buildable_list = [house, tree, fountain, hunting_shed]