from __future__ import annotations

from dataclasses import dataclass
from weakref import WeakValueDictionary


import PIL
import PIL.Image
import numpy as np

import arcade
from arcade.texture import (
    ImageData,
    Texture,
    make_circle_texture,
    make_soft_circle_texture,
)
from arcade.types import RGBA255, Color
from arcade.types.rect import Rect

@dataclass
class Grid:
    size: int
    sprite_list: arcade.SpriteList
    
    def __post_init__(self):
        size = self.size
        for a in range(50):
            for b in range(50):
                # arcade.draw_lbwh_rectangle_outline(a*size,b*size,size,size,arcade.csscolor.WHEAT,border_width=2)
                # g = GridSquare.from_grid_lbs(a*size,b*size,size)
                self.sprite_list.append(SpriteOutline(width=size, height=size,center_x=(size+2)*a,center_y=(size+2)*b+50))
                # self.sprite_list.append(SquareOutlineSprite(left=size*a, bottom=size*b, width=size, border_width=1, color=arcade.color.WHITE))

    def give_list(self):
        return(self.sprite_list)



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