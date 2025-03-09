from dataclasses import dataclass

@dataclass
class Buildable:
    """Class for holding things than can be built."""
    name: str
    cost: int
    upkeep: int
    image_path: str

@dataclass
class Town:
    """Class for tracking the economy of the town."""
    population: int
    money: float
    happiness: float
    jank: float
    things: list[Buildable]


house = Buildable(name='house', cost=10, upkeep=10, image_path="assets/outdoor/house.png")
tree = Buildable(name='tree', cost=1, upkeep=0, image_path="assets/outdoor/oak_tree.png")
buildable_list = [house, tree]