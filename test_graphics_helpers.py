import graphics_helpers as gh
import numpy as np
from numpy.testing import assert_array_equal

def test_square():
    o = np.array([0,0,0,0])
    x = np.array([255,255,255,255])
    test_array_border_3_1 = np.array([[x,x,x],
                                      [x,o,x],
                                      [x,x,x]])
    assert_array_equal(test_array_border_3_1, gh.create_square_border_array(size=3,border_width=1))
    test_array_border_6_2 = np.array([[x,x,x,x,x,x],
                                      [x,x,x,x,x,x],
                                      [x,x,o,o,x,x],
                                      [x,x,o,o,x,x],
                                      [x,x,x,x,x,x],
                                      [x,x,x,x,x,x],])
    assert_array_equal(test_array_border_6_2, gh.create_square_border_array(size=6,border_width=2))

    
