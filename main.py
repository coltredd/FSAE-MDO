from tireModel import calculateMu
import lapsim as lap
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import minimize, differential_evolution
import time
import itertools
import pandas as pd
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
    if 2*(timeCorner+timeStraight) > 55:
        return 2*(timeCorner+timeStraight)
    
    else:
        return 66
    


## def moment of inertia calc

def inertiaYaw(x,mass=240):
    Lwb = x[4]
    xCG = x[0]
    
    inertia = mass*(((Lwb**2)/12)+((Lwb/2)-xCG)**2)

    return inertia

## define Hessian trace calculator

def hessDiag(func,x,step):
    diagonals = []
    den = (1/(step**2))
    
    for n in range(len(x)):
        xLow = x[:]
        xHigh = x[:]   
        xLow[n] -= step
        xHigh[n] += step
        num = func(xHigh)-2*func(x)+func(xLow)
        hess = num/den
        diagonals.append(hess)
        print(xLow)
    return diagonals
## define parameter 




# layout constraints

def constraintWB(x):
    xVal = x[4]
    return xVal-1.525

def constraintY(x):
    xVal = x[1]
    return xVal

vMax = ( 75 ) / 2.237 # max speed of vehicle converted from ( MPH ) to m/s 

# bounds = [(.2,1.0),(0,0),(.1,.5),(.75,1.8),(1.5,1.9)]

# initialPoint = [.734,0,.292,1.27,1.53]
# search = np.linspace(.1,.5,100)
# valTime = []
# for n in search:
#     initialPoint[2] = n
#     valTime.append(simulate(initialPoint))
# fig = plt.figure(5)
# ax = fig.add_subplot(111)
# ax.scatter(search,valTime)
# plt.show()
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

def optimizeLap(startingPoint, method='SLSQP',max_iter=1e3):

    bounds = [(.2,1.0),(-.1,.1),(.1,.5),(.75,1.8),(1.2,2)] # bounds for the algo X,Y,Z, Ltw, Lwb
 
    constraints = [{'type':'ineq','fun': constraintWB},
                   {'type':'eq',  'fun': constraintY}]

    result = minimize(simulate,startingPoint,method=method, bounds = bounds,
                       constraints = constraints, options = {'maxiter': max_iter, 'disp': True})
    
    return result

def optimizeYaw(startingPoint, method='SLSQP',max_iter=1e3):

    bounds = [(.2,1.0),(-.1,.1),(.1,.5),(.75,1.8),(1.2,2)] # bounds for the algo X,Y,Z, Ltw, Lwb
 
    constraints = [{'type':'ineq','fun': constraintWB},
                   {'type':'eq',  'fun': constraintY}]

    result = minimize(inertiaYaw,startingPoint,method=method, bounds = bounds,
                       constraints = constraints, options = {'maxiter': max_iter, 'disp': True})
    
    return result


initialPoint = [.734,0,.292,1.27,1.53]
# print(simulate(initialPoint))
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


# check scaling need
# hessX = [.9,0,.1,1.8,1.6444]
# print(hessDiag(simulate,hessX,.00001))

# scaledXinitial = [.734e-3,0,.292e-3,1.27e-3,1.53e-3]
# result = optimizeLap(scaledXinitial)
# print(result.x)

# fuck it we GA now


# result = differential_evolution(simulate, bounds, maxiter=500,strategy='best2exp')
# print(result.x)
# print(result.fun)

# optimize Inertia

# resultYaw = optimizeYaw(initialPoint)
# print(resultYaw.x)

# resultTime = optimizeLap(initialPoint)
# print(resultTime.x)


def generate_random_point(bounds):
    return [np.random.uniform(low=bound[0], high=bound[1]) for bound in bounds]

def bigData(bounds,num):

    points = [generate_random_point([bounds[0],bounds[1],bounds[2],bounds[3],bounds[4]]) for _ in range(num)]

    results = []
    end = len(points)
    i = 0
    for point in points:
        result = {'x1': point[0], 'x2': point[1], 'x3': point[2], 'x4': point[3], 'x5': point[4],
                  'J1': simulate(point), 'J2': inertiaYaw(point)}
        results.append(result)
        i+=1
        print(i*100/num)

    return results

def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to '{filename}'.")

bounds = [(.2,.8),(-.1,.1),(.1,.4),(1,1.8),(1.525,2)]
num = 2500
# Perform full factorial exploration
results = bigData(bounds,num)


# Save results to a CSV file
filename = 'full_factorial_results.csv'
save_results_to_csv(results, filename)