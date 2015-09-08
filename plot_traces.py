import numpy
import sys 
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


# All units are in m!

# input constraints
terrainLength = 110                          # how long is the are of interest
goalAltitude = 2
d_up = 0.25                                # simplified rising/sinking of AUV, in metres per forward metre


# arrays for caclulations
terrain = [0.0] * (terrainLength + 150)        # initialise terrain with enough space to have flat surface in the long range measurements
horizonFollowing = [0] * terrainLength
optimum = [0.0] * terrainLength


# terrain definition

terrain[15] = 1.75
terrain[16] = 1.75
terrain[17] = 1.75
terrain[18] = 1.8

terrain[21] = 0.75
terrain[22] = 2.25
terrain[23] = 0.25


terrain[30] = 0.5
terrain[32] = 1

terrain[41] = 0.1
terrain[42] = 0.2
terrain[43] = 0.3
terrain[44] = 0.4
terrain[45] = 0.5
terrain[46] = 0.6
terrain[47] = 0.7
terrain[48] = 0.8
terrain[49] = 0.9
terrain[50] = 1.3



SONAR_DISTANCE = []
for i in range(150):
    altitude_range = numpy.sqrt(1-numpy.sin(i/150.)**2) * 150
    SONAR_DISTANCE.append(altitude_range)

def get_optimum(optimum, terrain):

    """
    Calculate the optimum path, so that every top is reached at the goal altitude

    Approach:
    copy terrain with added goal altitude
    check if all rise hights are below the maximum possible rise hight

    if not, start with the hightest jump and add rising steps beofre or after
    """

    optimum_found = 0

    # initialise with minimum distance, ignoring maximum raise speed
    for idx, o in enumerate(optimum):
        optimum[idx] = terrain[idx] + goalAltitude

    print(optimum)

    while optimum_found < 1:
        step = []
        previous = optimum[0]
        for m in optimum[1:]:
            step.append(m - previous)
            previous = m

        # check if all steps are reasonable
        if max(step) <= d_up and min(step) >= -d_up:
            optimum_found = 1
            print("f")
            break

        # find optimum path
        if max(step) >= - min(step):
            repair_idx = numpy.argmax(step) 
        else:
            repair_idx = numpy.argmin(step)

        riseSteps = int(round(abs(step[repair_idx])/d_up + 0.5))   # step needs to be positive and int; the number of stepse needs rounding up always

        if step[repair_idx] > d_up:
            for k in range(riseSteps):
                try:
                    if optimum[repair_idx-k +1 ] < optimum[repair_idx +1] -  d_up * k:
                        optimum[repair_idx-k +1 ] = optimum[repair_idx + 1] - d_up * k
                except:
                    pass
        if step[repair_idx] < -d_up:
            for k in range(riseSteps):
                try:
                    if optimum[repair_idx+k ] < optimum[repair_idx] - d_up * k:
                        optimum[repair_idx+k ] = optimum[repair_idx] - d_up * k
                except:
                    pass
        print(optimum)
    return optimum
    

def optimum_check(optimum, check):
    for i in optimum:
        check.append(i - goalAltitude)
    return check

def horizonFollow():
    horizonFollowing[0] = terrain[0] + goalAltitude
    for idx, a in enumerate(terrain[1:-150], 1):
        horizon = 0
        for o in range(150):
            if SONAR_DISTANCE[o] + terrain[idx-1] > terrain[idx + o]:
                if terrain[idx + o] > horizon:
                    horizon = terrain[idx + o]
                    print(horizon)
        if horizon + goalAltitude > horizonFollowing[idx-1]:
            horizonFollowing[idx] = horizonFollowing[idx - 1] + d_up
        elif horizon + goalAltitude < horizonFollowing[idx-1]:
            horizonFollowing[idx] = horizonFollowing[idx - 1] - d_up
        else:
            horizonFollowing[idx] = horizonFollowing[idx - 1]


    


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')


    optimum = get_optimum(optimum, terrain)

    check = []
    check = optimum_check(optimum, check)

    plt = pg.plot()
    plt.setWindowTitle('Terrain Following')
    plt.addLegend()

    plt.setLabel('left', "Altitude above lowest point in terrain", units='m')
    plt.setLabel('bottom', "Distance from start of terrain", units='m')

    plt.setLabel('top', '<br> <br> <br> Simplified visualisation of different terrain following algorithms. <br> <br> Assumptions: Decisions are made after each 1 m step; Maximum upwards speed of vehicle is constant at 0.25 m/s <br>')


    l = pg.LegendItem((400,60), offset=(70,30))  # args are (size, offset)
    l.setParentItem(plt.graphicsItem())   # Note we do NOT call plt.addItem in this case




    horizonFollow()

    c1Pen = pg.mkPen('k', width=3)  
    c1 = plt.plot(terrain[0:terrainLength], pen=c1Pen)
    l.addItem(c1, 'Terrain')
    c2Pen = pg.mkPen('g', width=3)  

    c2 = plt.plot(optimum, pen=c2Pen)
    l.addItem(c2, 'Optimum path considering maximum upwards speed')
    c3Pen = pg.mkPen('b', width=3)  
    c3 = plt.plot(check, pen= c3Pen)
    l.addItem(c3, 'Sanity check of optimum path: <br> Optimum path with the goal altitude substracted')
    c4Pen = pg.mkPen('r', width=3)  
    c4 = plt.plot(horizonFollowing, pen = c4Pen)
    l.addItem(c4, 'Horizon following, <br> assuming that at every step <br> the horizon is determined accurately <br>(!!! CURRENTLY INCORRECT!)')
 
    #c5 = plt.plot(SONAR_DISTANCE)



    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

