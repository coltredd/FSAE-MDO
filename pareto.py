import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("full_factorial_results.csv")

J1 = data['J1'].values
J2 = data['J2'].values

# plot the whole space
plt.figure(1)
plt.plot(J1,J2,'bo')
plt.xlim(55,120)
plt.ylim(bottom=40)
plt.xlabel('Lap Time [s]')
plt.ylabel('Yaw Inertia [kg-m^2]')
plt.title('Objective Space')
plt.show()
# calculate non dominated values

points = data[['J1','J2']].values.tolist()
def is_dominated(point, points):
    """
    Check if a point is dominated by any other point in a list of points.
    """
    for other_point in points:
        if all(x >= y for x, y in zip(point, other_point)) and any(x > y for x, y in zip(point, other_point)):
            return True
    return False
pointX = []
pointY = []
def find_non_dominated_points(points):
    """
    Find non-dominated points from a list of points.
    """
    non_dominated = []
    for point in points:
        if not is_dominated(point, points):
            non_dominated.append(point)
            pointX.append(point[0])
            pointY.append(point[1])
    return non_dominated

non_dominated_points = find_non_dominated_points(points)
plt.figure(2)
plt.plot(J1,J2,'bo')
plt.xlim(59.6,60.6)
plt.ylim(46.3,53)
plt.plot(pointX,pointY,'r*',markersize=20)
plt.xlabel('Lap Time [s]')
plt.ylabel('Yaw Inertia [kg-m^2]')
plt.title('Pareto Front')
plt.show()

