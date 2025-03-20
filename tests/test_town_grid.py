from nice_town_dude.town_grid import TownGridLogic, LandType
import numpy as np


def test_town_grid():
    tg = TownGridLogic(grid_size=(5, 5))
    assert tg.grid_size == (5, 5)
    assert np.all(tg.grid_array == LandType.CLEAR)
    assert tg.check_build_on_tiles((0, 0), (5, 5)) == True
    tg.reassign_tiles((1, 1), (2, 2), LandType.BUILDING)
    assert np.all(tg.grid_array[1:3, 1:3] == LandType.BUILDING)
    o = LandType.CLEAR
    x = LandType.BUILDING
    test_array = np.array(
        [
            [o, o, o, o, o],
            [o, x, x, o, o],
            [o, x, x, o, o],
            [o, o, o, o, o],
            [o, o, o, o, o],
        ]
    )
    assert np.array_equal(tg.grid_array, test_array)
    assert tg.check_build_on_tiles((3, 3), (2, 2)) == True
    assert tg.check_build_on_tiles((0, 0), (2, 2)) == False
    tg.reassign_tiles((3, 3), (1, 1), LandType.BUILDING)
    tg.reassign_tiles((1, 0), (1, 1), LandType.BUILDING)
    tg.reassign_tiles((3, 1), (1, 1), LandType.BUILDING)

    test_array = np.array(
        [
            [o, o, o, o, o],
            [x, x, x, o, o],
            [o, x, x, o, o],
            [o, x, o, x, o],
            [o, o, o, o, o],
        ]
    )
    assert np.array_equal(tg.grid_array, test_array)
