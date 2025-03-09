"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade
from town import Town

# Constants
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240
WINDOW_TITLE = "Nice Town Dude"
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

        # self.set_texture(texture_list[0])
        # if self.time_elapsed > 0.1:
        #     if self.cur_texture_index < len(self.textures):
        #         self.set_texture(self.cur_texture_index)  
        #         self.cur_texture_index += 1  
        #     self.time_elapsed = 0

        # if self.cur_texture_index == 5:
        #     self.cur_texture_index = 0

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
            # print("move down")
            self.curr_texture_list = self.face_down
        # print(self.curr_texture_list)
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
        self.bottom_text = "foo"
        self.town = Town(population=1, money=100, happiness=10, jank=10)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass
    
    def update_text(self):
        self.bottom_text = f"Pop: {self.town.population} | $: {self.town.money} | :) {self.town.happiness} | Jank: {self.town.jank}"

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()
        self.sprite_list.sort(key=lambda x: x.bottom, reverse=True)    
        self.sprite_list.draw()
        self.update_text()
        arcade.draw_text(self.bottom_text,10,10)



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
            self.build_house(location=self.player.position)
            
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
    
    def build_house(self, location: tuple[int, int]):
        house = arcade.Sprite("assets/outdoor/house.png")
        house.position = location
        house.depth = 100
        self.sprite_list.append(house)
        self.town.money -= 100


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()