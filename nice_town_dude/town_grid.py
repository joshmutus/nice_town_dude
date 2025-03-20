import numpy as np
from dataclasses import dataclass
from enum import Enum

class LandType(Enum):
    CLEAR = 0
    GRASS = 1
    TREE = 2
    ROAD = 3
    BUILDING = 4

@dataclass
class TownGrid:
    grid_size: tuple[int, int] = (50, 50)

    def __post_init__(self):
        self.grid_array = np.full(self.grid_size, LandType.CLEAR)


    def check_build_on_tiles(self, bl: tuple[int, int], size: tuple[int, int]) -> bool:
        """
        Checks if all tiles within a specified rectangular area are of type GRASS.

        Buildable tiles are grass for now.

        Args:
            bl (tuple[int, int]): The bottom-left corner of the rectangle, specified as (row, column).
            tr (tuple[int, int]): The top-right corner of the rectangle, specified as (row, column).

        Returns:
            bool: True if all tiles in the specified area are of type GRASS, False otherwise.
        """
        tr = (bl[0]+size[0], bl[1]+size[1])
        if np.all(self.grid_array[bl[0]:tr[0], bl[1]:tr[1]] == LandType.CLEAR):
            print(bl,tr)
            print(self.grid_array[bl[0]:tr[0], bl[1]:tr[1]] )
            return True
        return False
    
    def reassign_tiles(self, bl: tuple[int, int], size: tuple[int, int], land_type: LandType) -> None:
        self.grid_array[bl[0]:bl[0]+size[0], bl[1]:bl[0]+size[0]] = land_type