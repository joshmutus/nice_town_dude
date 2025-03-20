
from dataclasses import dataclass

from nice_town_dude.custom_sprites import SpriteOutline
from nice_town_dude.town_grid import TownGrid
import arcade


@dataclass
class Grid:
    size: int
    sprite_list: arcade.SpriteList

    def __post_init__(self):  
        size = self.size
        for a in range(50):
            for b in range(50):
                self.sprite_list.append(SpriteOutline(width=size, height=size,center_x=(size+2)*a,center_y=(size+2)*b+50))

    def give_list(self):
        return(self.sprite_list)



