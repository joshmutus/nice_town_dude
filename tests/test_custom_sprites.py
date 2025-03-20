from nice_town_dude.custom_sprites import create_square_border_array, Building
from nice_town_dude.town import CharSheet
import numpy as np
from numpy.testing import assert_array_equal


def test_square():
    o = np.array([0, 0, 0, 0])
    x = np.array([255, 255, 255, 255])
    test_array_border_3_1 = np.array([[x, x, x], [x, o, x], [x, x, x]])
    assert_array_equal(
        test_array_border_3_1, create_square_border_array(size=3, border_width=1)
    )
    test_array_border_6_2 = np.array(
        [
            [x, x, x, x, x, x],
            [x, x, x, x, x, x],
            [x, x, o, o, x, x],
            [x, x, o, o, x, x],
            [x, x, x, x, x, x],
            [x, x, x, x, x, x],
        ]
    )
    assert_array_equal(
        test_array_border_6_2, create_square_border_array(size=6, border_width=2)
    )


def test_building():
    char_sheet = CharSheet(path="tests/test_sheet.png", columns=2, count=10)
    test_building = Building(char_sheet_spec=char_sheet)
    assert len(test_building.texture_list) == 10
    assert test_building.dirty == 0
    test_building.increase_dirt()
    assert test_building.dirty == 1
    test_building.decrease_dirt()
    assert test_building.dirty == 0
    test_building.decrease_dirt()
    assert test_building.dirty == 0
    for a in range(10):
        test_building.increase_dirt()
    assert test_building.dirty == 9
    test_building.increase_dirt()
    assert test_building.dirty == 9
    test_building.reset_dirt()
    assert test_building.dirty == 0
    # TODO test that images correspond as well
