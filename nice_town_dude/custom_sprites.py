from __future__ import annotations

import arcade
from arcade.texture import (
    ImageData,
    Texture
)
from arcade.types import RGBA255, Color
from arcade.types.rect import Rect
from weakref import WeakValueDictionary


import PIL
import PIL.Image
import numpy as np

from town import CharSheet

class Building(arcade.Sprite):     
    """Sprite for buildings."""      
    def __init__(self, char_sheet_spec: CharSheet, size=32, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)        
        char_sheet  = arcade.load_spritesheet(char_sheet_spec.path)
        self.texture_list = char_sheet.get_texture_grid(size=(size, size), columns=char_sheet_spec.columns, count=char_sheet_spec.count)
        self.texture = self.texture_list[0]
        self.cleanliness = 0
    
    def increment_cleanliness(self):
        self.cleanliness += 1

    def reset_cleanliness(self):
        self.cleanliness = 0

class Player(arcade.Sprite):
    def __init__(self, char_sheet_spec: CharSheet, size=32):
        super().__init__()
        char_sheet  = arcade.load_spritesheet(char_sheet_spec.path)
        texture_list = char_sheet.get_texture_grid(size=(size, size), columns=char_sheet_spec.columns, count=char_sheet_spec.count)
        self.textures = texture_list
        self.time_elapsed = 0
        self.cur_texture_index = 0
        self.face_down = list(range(6))
        self.face_right = list(range(6,12))
        self.face_up = list(range(12,18))
        self.face_left = list(range(18,24))
        self.curr_texture_list = []
    
    def iterate_texture(self) -> None:
        self.set_texture(self.cur_texture_index)
        if self.cur_texture_index < self.curr_texture_list[0]:
            self.cur_texture_index = self.curr_texture_list[0]
        elif self.cur_texture_index > self.curr_texture_list[-1]-1:
            self.cur_texture_index = self.curr_texture_list[0]
        else:
            self.cur_texture_index += 1

    def update(self, delta_time = 1 / 60, *args, **kwargs) -> None:
        self.time_elapsed += delta_time 
        if self.time_elapsed > 0.1:
            self.iterate_texture()
            self.time_elapsed = 0

        # Move player.
        if self.change_x > 0:
            self.curr_texture_list = self.face_right
        elif self.change_x < 0:
            self.curr_texture_list = self.face_left
        elif self.change_y > 0:
            self.curr_texture_list = self.face_up
        else:
            self.curr_texture_list = self.face_down
        self.center_x += self.change_x
        self.center_y += self.change_y
    
class SpriteOutline(arcade.Sprite):
    """Copied and modified from SpriteSolid. Probably lots of cruft to remove"""
    __slots__ = ()
    _default_image: ImageData | None = None
    # To avoid making lots of texture instances with the same configuration
    # we cache them here weakly. Making a 100 x 100 grid of white sprites
    # only create 1 texture instead of 1000. This saves memory and processing
    # time for the default texture atlas.
    _texture_cache: WeakValueDictionary[tuple[int, int], Texture] = WeakValueDictionary()

    def __init__(
        self,
        width: int,
        height: int,
        center_x: float = 0,
        center_y: float = 0,
        color: RGBA255 = Color(255, 255, 255, 255),
        angle: float = 0,
        **kwargs,
    ):
        texture = self.__class__._texture_cache.get((width, height))
        if texture is None:
            texture = Texture(
                self._get_default_image(),
                hit_box_points=(
                    (-width / 2, -height / 2),
                    (width / 2, -height / 2),
                    (width / 2, height / 2),
                    (-width / 2, height / 2),
                ),
            )
            texture.size = width, height
            self.__class__._texture_cache[(width, height)] = texture

        super().__init__(
            texture,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
        )
        self.default_texture = self.texture
        self.color = Color.from_iterable(color)
        self.collision_texture = arcade.Texture(self.create_on_collision_image(),
                                                hit_box_points=(
                                                    (-width / 2, -height / 2),
                                                    (width / 2, -height / 2),
                                                    (width / 2, height / 2),
                                                    (-width / 2, height / 2),
                                                    ),
                                                    )
        self.collision_texture.size = width, height

    @classmethod
    def from_rect(cls, rect: Rect, color: Color, angle: float = 0.0) -> SpriteOutline:
        """
        Construct a new SpriteSolidColor from a :py:class:`~arcade.types.rect.Rect`.

        Args:
            rect:
                The rectangle to use for the sprite's dimensions and position.
            color:
                The color of the sprite as a :py:class:`~arcade.types.Color`,
                an RGBA tuple, or an RGB tuple.
            angle:
                The angle of the sprite in degrees.
        """
        return cls(int(rect.width), int(rect.height), rect.x, rect.y, color, angle)

    def _get_default_image(self) -> ImageData:
        """Lazy-load the default image for this sprite type."""
        im = self.__class__._default_image
        im_array = create_square_border_array(32, border_width=2, border_color=(255,255,255,255))
        if im is None:
            im = ImageData(
                PIL.Image.fromarray(im_array),
                hash="sprite_outline",
            )
            self.__class__._default_image = im
        return im
    
    def change_grid_color(self):
        self.texture = self.collision_texture
    
    def reset_texture(self):
        self.texture = self.default_texture
    
    def create_on_collision_image(self) -> ImageData:
        im_array = create_square_border_array(32, border_width=2, border_color=(255,0,0,255))
        im = ImageData(
                PIL.Image.fromarray(im_array),
                hash="sprite_outline_highlight",
            )
        return im
    
def create_square_border_array(size, border_width=1, border_color=(255,255,255,255)):
    default_value = (0,0,0,0)
    border_color = border_color
    a = np.full((size,size,4),default_value,dtype=np.uint8)
    a[0:border_width, :] = border_color  # Top row
    a[-(border_width):, :] = border_color # Bottom row
    a[:, 0:border_width] = border_color  # Left column
    a[:, -(border_width):] = border_color # Right column
    return a