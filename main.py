from tireModel import calculateMu
import lapsim as lap
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import minimize
import time
def simulate(x):
    params = {
    'track' : {
        'straight' : 250, # length of straight in meters
        'radius'   : 25 # radius of corner in meters
    },
    'car' : {
        'mass'      : 240, # mass of vehicle in kilograms
        'wheelbase' : x[4],
        'trackwidth': x[3],
        'CG'        : [x[0],x[1],x[2]] # location of center of gravity X,Y,Z in meters as defined by coordinate system
    }
}
    vEntry,timeCorner = lap.timeCornerCalc(params)

    timeStraight = lap.timeStrightCalc(vEntry,vMax,params)

    return 2*(timeCorner+timeStraight)

## define parameter 

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


# layout constraints

def constraintWB(x):
    xVal = x[4]
    return xVal-1.525

def constraintY(x):
    xVal = x[1]
    return xVal

vMax = ( 75 ) / 2.237 # max speed of vehicle converted from ( MPH ) to m/s 
# # search = np.linspace(-.2,.2,100)
# # valTime = []
# # for n in search:
# #     params['car']['CG'][1] = n
# #     valTime.append(simulate(params))
# # fig = plt.figure(5)
# # ax = fig.add_subplot(111)
# # ax.scatter(search,valTime)
# # plt.show()
# t1 = time.perf_counter()
# simulate(params)
# print(simulate(params))
# t2 = time.perf_counter()

# print('Time it took to run: ', t2-t1)

# ## Conduct DOE

# generate full factorial levels = 3, variables = 5 (x,y,z,Ltw,Lwb)
# import itertools
# levels = [-1,0,1]
# combo = list(itertools.product(levels,repeat=5))
# i = 1
# # print(len(combo))
# # loop through full factorial set
# for sets in combo:

#     # set variables to change in params

#     params['car']['CG'][0] = sets[0] * 0.3 + .734
#     params['car']['CG'][1] = sets[1] * 0.2
#     params['car']['CG'][2] = sets[2] * .1 + .292
#     params['car']['trackwidth'] = sets[3] * (0.23) + 1.270
#     params['car']['wheelbase'] = sets[4] * (0.23) + 1.76
#     print(sets[0] * 0.3 + .734,sets[1] * 0.2,sets[2] * .1 + .292,sets[3] * (0.23) + 1.270,sets[4] * (0.23) + 1.76,simulate(params))
#     # simulate(params)
#     # print(i/243*100,'% Done')
#     # i += 1

### END OF DOE

# OPTIMIZER

# def optimizeLap(startingPoint, method='SLSQP',max_iter=1e3):

#     bounds = [(.2,1.0),(-.1,.1),(.1,.5),(.75,1.8),(1.2,2)] # bounds for the algo X,Y,Z, Ltw, Lwb
 
#     constraints = [{'type':'ineq','fun': constraintWB},
#                    {'type':'eq',  'fun': constraintY}]

#     result = minimize(simulate,startingPoint,method=method, bounds = bounds,
#                        constraints = constraints, options = {'maxiter': max_iter, 'disp': True})
    
#     return result
initialPoint = [.734,0,.292,1.27,1.53]
print(simulate(initialPoint))
# result = optimizeLap(initialPoint)
# print(result.x)
# print(result.jac)


# results = []
# num_runs = 10
# # multistart that jawn
# for run in range(num_runs):
    
#     initialPoint = np.random.uniform([.2,-.1,.1,.75,1.2],[1,.1,.5,1.8,2])

#     result = optimizeLap(initialPoint)
#     results.append({
#         'starting_point': initialPoint,
#         'iterations': result.nit,
#         'Final Point': result.x,
#         'Obj' : result.fun,
#         'Feasible': result.success
#     })

# for i, res in enumerate(results):
#     print(f"Run {i+1}:")
#     print(f"    Start: {res['starting_point']}")
#     print(f"    Final point: {res['Final Point']}")
#     print(f"    Objective Function Value: {res['Obj']}")
#     print(f"  Feasible: {res['Feasible']}")
