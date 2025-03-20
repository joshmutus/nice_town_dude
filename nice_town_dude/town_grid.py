import numpy as np
import arcade
from dataclasses import dataclass
from nice_town_dude.custom_sprites import SpriteOutline
from nice_town_dude.town import LandType

@dataclass
class Grid:
    size: int
    sprite_list: arcade.SpriteList

    def __post_init__(self):  
        size = self.size
        self.grid_logic = TownGridLogic(grid_size=(size,size))
        for a in range(size):
            for b in range(size):
                self.sprite_list.append(SpriteOutline(width=size, height=size,center_x=(size)*a,center_y=(size)*b, grid_coord=(a,b)))

    def give_list(self):
        return(self.sprite_list)
    
    

@dataclass
class TownGridLogic:
    """Thing for handling the logic of the town grid."""
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