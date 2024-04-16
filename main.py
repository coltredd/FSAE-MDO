from tireModel import calculateMu
import lapsim as lap
import numpy as np 
import matplotlib.pyplot as plt 

def simulate(params):

    vEntry,timeCorner = lap.timeCornerCalc(params)

    timeStraight = lap.timeStrightCalc(vEntry,vMax,params)

    return 2*(timeCorner+timeStraight)


params = {
    'track' : {
        'straight' : 250, # length of straight in meters
        'radius'   : 25 # radius of corner in meters
    },
    'car' : {
        'mass'      : 240, # mass of vehicle in kilograms
        'wheelbase' : 1.530,
        'trackwidth': 1.270,
        'CG'        : [.734,0,.292] # location of center of gravity X,Y,Z in meters as defined by coordinate system
    }
}

vMax = ( 75 ) / 2.237 # max speed of vehicle converted from ( MPH ) to m/s 
search = np.linspace(-.2,.2,100)
valTime = []
for n in search:
    params['car']['CG'][1] = n
    valTime.append(simulate(params))
fig = plt.figure(5)
ax = fig.add_subplot(111)
ax.scatter(search,valTime)
plt.show()
print(simulate(params))