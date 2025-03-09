import math
from dataclasses import dataclass

@dataclass
class Town:
    """Class for tracking the economy of the town"""
    population: int
    money: float
    happiness: float
    jank: float



