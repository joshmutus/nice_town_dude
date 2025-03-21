from __future__ import annotations

from nice_town_dude.town import CharSheet

import arcade
from arcade.texture import ImageData, Texture
from arcade.types import RGBA255, Color
from arcade.types.rect import Rect
import itertools
from weakref import WeakValueDictionary

import PIL
import PIL.Image
import numpy as np


class Building(arcade.Sprite):
    """Sprite for buildings."""

    def __init__(
        self,
        char_sheet_spec: CharSheet,
        size=32,
        path_or_texture=None,
        scale=1,
        center_x=0,
        center_y=0,
        angle=0,
        **kwargs,
    ):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        char_sheet = arcade.load_spritesheet(char_sheet_spec.path)
        self.texture_list = char_sheet.get_texture_grid(
            size=(size, size),
            columns=char_sheet_spec.columns,
            count=char_sheet_spec.count,
        )
        self.dirty = 0
        self.texture = self.texture_list[self.dirty]

    def increase_dirt(self):
        if self.dirty < len(self.texture_list) - 1:
            self.dirty += 1
            self.texture = self.texture_list[self.dirty]

    def decrease_dirt(self):
        if self.dirty > 0:
            self.dirty -= 1
            self.texture = self.texture_list[self.dirty]

    def reset_dirt(self):
        self.dirty = 0
        self.texture = self.texture_list[self.dirty]


class Player(arcade.Sprite):
    def __init__(
        self,
        char_sheet_spec: CharSheet,
        size=32,
        path_or_texture=None,
        scale=1,
        center_x=0,
        center_y=0,
        angle=0,
        **kwargs,
    ):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        char_sheet = arcade.load_spritesheet(char_sheet_spec.path)
        texture_list = char_sheet.get_texture_grid(
            size=(size, size),
            columns=char_sheet_spec.columns,
            count=char_sheet_spec.count,
        )
        self.textures = texture_list
        self.set_texture(0)
        self.time_elapsed = 0
        self.cur_texture_index = 0
        self.idle = itertools.cycle([0, 19, 20])
        self.walk_down = itertools.cycle([0, 1, 2, 3, 4, 5, 6])
        self.walk_right = itertools.cycle([11, 12, 13, 14])
        self.walk_up = itertools.cycle([7, 8, 9, 10])
        self.walk_left = itertools.cycle([15, 16, 17, 18])
        self.curr_texture_iter = self.idle
        print(f"there are this many textures: {len(self.textures)}")

    def update(self, delta_time=1 / 60, *args, **kwargs) -> None:
        self.time_elapsed += delta_time
        if self.time_elapsed > 0.05:
            next_texture = next(self.curr_texture_iter)
            self.set_texture(next_texture)
            self.time_elapsed = 0

        # Move player.
        if self.change_x > 0:
            self.curr_texture_iter = self.walk_right
        elif self.change_x < 0:
            self.curr_texture_iter = self.walk_left
        elif self.change_y > 0:
            self.curr_texture_iter = self.walk_up
        elif self.change_y < 0:
            self.curr_texture_iter = self.walk_down
        else:
            self.curr_texture_iter = self.idle
        self.center_x += self.change_x
        self.center_y += self.change_y


class InvisibleCollisionSprite(arcade.Sprite):
    def __init__(
        self,
        width: int,
        height: int,
        center_x: float = 0,
        center_y: float = 0,
        **kwargs,
    ):
        texture = Texture(
            ImageData(
                PIL.Image.new("RGBA", (width, height), (0, 0, 0, 0)),
                hash="invisible_collision",
            ),
            hit_box_points=(
                (-width / 2, -height / 2),
                (width / 2, -height / 2),
                (width / 2, height / 2),
                (-width / 2, height / 2),
            ),
        )
        texture.size = width, height
        super().__init__(
            texture,
            center_x=center_x,
            center_y=center_y,
        )


class SpriteOutline(arcade.Sprite):
    """Copied and modified from SpriteSolid. Probably lots of cruft to remove"""

    __slots__ = ()
    _default_image: ImageData | None = None
    # To avoid making lots of texture instances with the same configuration
    # we cache them here weakly. Making a 100 x 100 grid of white sprites
    # only create 1 texture instead of 1000. This saves memory and processing
    # time for the default texture atlas.
    _texture_cache: WeakValueDictionary[tuple[int, int], Texture] = (
        WeakValueDictionary()
    )

    def __init__(
        self,
        width: int,
        height: int,
        grid_coord: tuple[int, int],
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
        self.collision_texture = arcade.Texture(
            self.create_on_collision_image(),
            hit_box_points=(
                (-width / 2, -height / 2),
                (width / 2, -height / 2),
                (width / 2, height / 2),
                (-width / 2, height / 2),
            ),
        )
        self.collision_texture.size = width, height
        self.grid_coord = grid_coord

    def _get_default_image(self) -> ImageData:
        """Lazy-load the default image for this sprite type."""
        im = self.__class__._default_image
        im_array = create_square_border_array(
            32, border_width=2, border_color=(255, 255, 255, 255)
        )
        if im is None:
            im = ImageData(
                PIL.Image.fromarray(im_array),
                hash="sprite_outline",
            )
            self.__class__._default_image = im
        return im

    def set_active_cell(self):
        self.texture = self.collision_texture
        return self.grid_coord

    def reset_texture(self):
        self.texture = self.default_texture

    def create_on_collision_image(self) -> ImageData:
        im_array = create_square_border_array(
            32, border_width=2, border_color=(255, 0, 0, 255)
        )
        im = ImageData(
            PIL.Image.fromarray(im_array),
            hash="sprite_outline_highlight",
        )
        return im


def create_square_border_array(size, border_width=1, border_color=(255, 255, 255, 255)):
    default_value = (0, 0, 0, 0)
    border_color = border_color
    a = np.full((size, size, 4), default_value, dtype=np.uint8)
    a[0:border_width, :] = border_color  # Top row
    a[-(border_width):, :] = border_color  # Bottom row
    a[:, 0:border_width] = border_color  # Left column
    a[:, -(border_width):] = border_color  # Right column
    return a
