import arcade
from nice_town_dude.town import Town, buildable_list, CharSheet
from nice_town_dude.graphics_helpers import Grid
from nice_town_dude.custom_sprites import Player, Building

# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Nice Town, Dude"
MOVEMENT_SPEED = 5
BASE_TILE_SIZE = 32
SCALE = 1 

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        print("init GameView")
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.sprite_list = arcade.SpriteList()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        player_sheet = CharSheet(path='assets/player/player.png', columns=6, count=36)
        self.draw_order = []
        self.player = Player(player_sheet, size=BASE_TILE_SIZE, scale=SCALE)
        self.player.position = 220,220
        self.sprite_list.append(self.player)
        self.bottom_text = ''
        self.town = Town(population=1, money=100, happiness=10, jank=10, things=[])
        self.build_list = buildable_list
        self.build_idx = 0
        self.show_grid = False
        self.grid_list = arcade.SpriteList()
        self.grid = Grid(size=20, sprite_list=self.grid_list)

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
        if self.show_grid:
            self.grid_list.draw()
        self.update_text()
        arcade.draw_text(self.bottom_text,10,10, arcade.color.DUTCH_WHITE)

    def on_update(self, delta_time: float) -> None:
        self.sprite_list.update() 
        collisions = arcade.check_for_collision_with_list(self.player, self.grid.sprite_list)
        for grid in self.grid.sprite_list:
            grid.reset_texture()
        if collisions:
            [cell.change_grid_color() for cell in collisions]

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
            self.show_grid = True
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

        if key == arcade.key.A:
            self.build_thing(location=self.player.position)
            self.show_grid = False
    
    def build_thing(self, location: tuple[int, int]):
        thing_to_build = self.build_list[self.build_idx]
        thing = Building(char_sheet_spec=thing_to_build.character_sheet, scale=SCALE)
        thing.position = location
        self.sprite_list.append(thing)
        self.town.money -= thing_to_build.cost
        self.town.things.append(thing_to_build)