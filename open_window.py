"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade
from town import Town, buildable_list

# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Nice Town, Dude"
MOVEMENT_SPEED = 5


class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0])
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
        # print(self.cur_texture_index)
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
    


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.sprite_list = arcade.SpriteList()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        char_sheet  = arcade.load_spritesheet("assets/player/player.png")
        self.draw_order = []
        self.texture_list = char_sheet.get_texture_grid(size=(32,32), columns=6, count=36)
        self.player = Player(self.texture_list)
        self.player.position = 200,200
        self.sprite_list.append(self.player)
        self.bottom_text = ''
        self.town = Town(population=1, money=100, happiness=10, jank=10, things=[])
        self.build_list = buildable_list
        self.build_idx = 0
        arcade.draw_rect_filled(arcade.rect.XYWH(100, 100, 30, 30),
                                arcade.csscolor.BLACK, 0)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass
    
    def update_text(self):
        self.bottom_text = f"Pop: {self.town.population} | $: {self.town.money} | Happiness: {self.town.happiness} | Jank: {self.town.jank} | Build: {self.build_list[self.build_idx].name}"

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.sprite_list.sort(key=lambda x: x.bottom, reverse=True)    
        self.sprite_list.draw()
        self.update_text()
        arcade.draw_text(self.bottom_text,10,10, arcade.color.DUTCH_WHITE)
        self.draw_grid(50)


    def on_update(self, delta_time: float) -> None:
        self.sprite_list.update() 

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

        if key == arcade.key.A:
            self.build_thing(location=self.player.position)
        if key == arcade.key.F:
            self.build_idx += 1
            self.build_idx = self.build_idx%len(self.build_list)
            
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
    
    def build_thing(self, location: tuple[int, int]):
        thing_to_build = self.build_list[self.build_idx]
        thing = arcade.Sprite(thing_to_build.image_path)
        thing.position = location
        self.sprite_list.append(thing)
        self.town.money -= thing_to_build.cost
        self.town.things.append(thing_to_build)

    def draw_grid(self, size):
        print("drawing grid")
        for a in range(10):
            for b in range(10):
                print(a,b)
                arcade.draw_lbwh_rectangle_outline(a*size,b*size,size,size,arcade.csscolor.WHEAT,border_width=2)




def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()