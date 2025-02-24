"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade

# Constants
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240
WINDOW_TITLE = "Strong Town"


class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0])
        self.textures = texture_list
        self.time_elapsed = 0

    def update(self, delta_time = 1 / 60, *args, **kwargs) -> None:
        self.time_elapsed += delta_time 

        if self.time_elapsed > 0.1:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)  
                self.cur_texture_index += 1  
            self.time_elapsed = 0

        if self.cur_texture_index == 23:
            self.cur_texture_index = 0

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.sprite_list = arcade.SpriteList()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        char_sheet  = arcade.load_spritesheet("assets/player/player_actions.png")
        self.texture_list = char_sheet.get_texture_grid(size=(48,48), columns=2, count=24)
        print("TEXTURE LEN: ", len(self.texture_list))
        self.player = Player(self.texture_list)
        self.player.position = 200,200
        self.sprite_list.append(self.player)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()
        self.sprite_list.draw()
        
        # Code to draw other things will go here

    def on_update(self, delta_time: float) -> None:
        self.sprite_list.update() 


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()