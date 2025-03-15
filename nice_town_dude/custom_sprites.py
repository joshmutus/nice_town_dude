import arcade

from town import CharSheet

class Building(arcade.Sprite):     
    """Sprite for buildings."""      
    def __init__(self, char_sheet_spec: CharSheet, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)        
        char_sheet  = arcade.load_spritesheet(char_sheet_spec.path)
        self.texture_list = char_sheet.get_texture_grid(size=(32,32), columns=char_sheet_spec.columns, count=char_sheet_spec.count)
        self.texture = self.texture_list[0]
        self.cleanliness = 0
    
    def increment_cleanliness(self):
        self.cleanliness += 1

    def reset_cleanliness(self):
        self.cleanliness = 0

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
    