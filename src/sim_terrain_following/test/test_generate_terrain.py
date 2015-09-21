from sim_terrain_following import analyse_terrain
from sim_terrain_following import generate_terrain as gt
import numpy

def test_basic():
    pass


def test_random_output_type():
    """
    All data that is read should be numpy!
    """
    assert isinstance(gt.generate_heights(2,1,1), numpy.ndarray)
    assert isinstance(gt.generate_slope(2,1,1), numpy.ndarray)

def test_random_output_length():
    """
    Check that the output arrays are indeed as long as requested
    """
    assert len(gt.generate_heights(10, 2, 2)) == 20
    assert len(gt.generate_slope(10, 2, 2)) == 20

def test_random_output_limits():
    """
    Check that the limitations (maximum terrain height or maximum slope) are kept
    and that no negative terrain points are returned
    """
    print("Careful, this test is run on random numbers, so errors might not reoccur")

    assert max(gt.generate_heights(10,20,2)) <= 2
    assert min(gt.generate_heights(10,20,2)) >= 0

    assert min(gt.generate_slope(10,20,2)) >= 0
    # generate_slope needs calculation of slope!
    t = gt.generate_slope(10,20,2)
    max_slope = 0
    for i, height in enumerate(t[1:]):
        slope = abs(height - t[i])  # i will count from 0, even though enumerate starts from 1!
        max_slope = max(slope, max_slope)
        # print some things that may help with debugging
        print("index: " + str(i))
        print("calculated slope: " + str(i))
        print("two compared values: " + str(height) + " " + str(t[i]))
    print(t)
 
    assert max_slope <= 2

