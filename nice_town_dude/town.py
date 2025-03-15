from dataclasses import dataclass
import arcade

@dataclass
class CharSheet:
    """Dataclass for holding character sheet attributes."""
    path: str
    columns: int
    count: int

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

@dataclass
class Buildable:
    """Class for holding things than can be built."""
    name: str
    cost: int
    upkeep: int
    character_sheet: CharSheet

@dataclass
class Town:
    """Class for tracking the economy of the town."""
    population: int
    money: float
    happiness: float
    jank: float
    things: list[Buildable]


house = Buildable(name='house', cost=10, upkeep=10, character_sheet=CharSheet(path="assets/outdoor/house_small.png", 
                                                                              columns=2, 
                                                                              count=6))
tree = Buildable(name='tree', cost=1, upkeep=0, character_sheet=CharSheet(path="assets/outdoor/oak_tree.png", 
                                                                          columns=1, 
                                                                          count=1))
fountain = Buildable(name='fountain', cost=20, upkeep=10, character_sheet=CharSheet(path="assets/outdoor/fountain.png", 
                                                                                    columns=1,
                                                                                    count=1))
hunting_shed = Buildable(name='hunting shed', cost=50, upkeep=5, character_sheet=CharSheet(path="assets/outdoor/hunting_shed.png", 
                                                                                           columns=1,
                                                                                           count=2))
buildable_list = [house, tree, fountain, hunting_shed]