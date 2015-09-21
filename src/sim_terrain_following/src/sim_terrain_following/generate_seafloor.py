import numpy


def generate_heights(length, resolution, max_height):
    """
    generate a random terrain based on the maximum height from 0 level
    """
    terrain = numpy.random.rand(length*resolution) * max_height
    return terrain

def generate_slope(length, resolution, max_slope):
    """
    generate a random terrain based on the maximum given slope
    """
    terrain = numpy.array([0])
    for t in range(length*resolution - 1):
        slope = numpy.random.rand(1) *2*max_slope - max_slope  #negative random numbers are not allowed
        terrain = numpy.append(terrain, [terrain[-1] + slope])
        terrain = terrain - min(terrain)
    return terrain

# TODO: Add read from file, for selection of file types
