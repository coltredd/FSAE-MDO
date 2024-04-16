import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Read data from CSV file
data = pd.read_csv("tires.csv")

# Extract slip angle, lateral force, and normal force data
slip_angle = data['Slip Angle'].values
normal_force = data['Normal Force'].values *-1 # Multiplies by -1 to flip the sign of normal force that exists in data set
lateral_force = data['Lateral Force'].values

# Polynomial regression
poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(np.column_stack((slip_angle, normal_force)))
regressor = LinearRegression()
regressor.fit(X_poly, lateral_force)

# Create meshgrid for plotting surface
slip_angle_grid, normal_force_grid = np.meshgrid(np.linspace(min(slip_angle), max(slip_angle), 100),
                                                 np.linspace(min(normal_force), max(normal_force), 100))
X_grid = poly.transform(np.array([slip_angle_grid.ravel(), normal_force_grid.ravel()]).T)
lateral_force_surface = regressor.predict(X_grid).reshape(slip_angle_grid.shape)

# # Plot 3D surface
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(slip_angle, normal_force, lateral_force, color='blue', label='Data')
# surf = ax.plot_surface(slip_angle_grid, normal_force_grid, lateral_force_surface, cmap='viridis', alpha=0.5, label='Surface')
# ax.set_xlabel('Slip Angle')
# ax.set_ylabel('Normal Force')
# ax.set_zlabel('Lateral Force')
# ax.legend()

# # Build Graph of Tire Coeff
minNorm = min(normal_force)
maxNorm = max(normal_force)
forceNormal = np.linspace(minNorm,maxNorm,100)

# Define slip angles for evaluation
slip_angles_eval = np.linspace(min(slip_angle), max(slip_angle), 100)

# Initialize arrays to store max lateral force and corresponding normal force

corresponding_normal_force = []
normal_force_pred = 500
# Iterate over slip angles and normal force to find corresponding lateral forces using the fitted surface
muList =[]
for force in forceNormal:
    max_lateral_force = []
    for angle in slip_angles_eval:
        # Predict lateral force using the fitted model
        X_pred = poly.transform([[angle, force]])
        lateral_force_pred = regressor.predict(X_pred)[0]
        
        # Append lateral force and corresponding normal force
        max_lateral_force.append(abs(lateral_force_pred))
    # Calculate effective coefficient of friction
    muEff = max(max_lateral_force)/force
    muList.append(muEff*.6)

hellabands = np.linspace(0,2000)
coeff = np.polyfit(forceNormal,muList,3)
func = np.poly1d(coeff)
# Plot the bitch
    
# fig = plt.figure(2)
# ax = fig.add_subplot(111)
# ax.scatter(forceNormal,muList)
# ax.set_xlabel("Normal Force")
# ax.set_ylabel("Mu")
# ax.scatter(forceNormal,func(forceNormal))
# plt.show()



### Future work note: create way to utilize this shit to handle a normal force using input into a function.
### Will use such function to calcuate grip levels
### Longitudinal forces are next, god help me



# def calculateMu(forceNormal):
#     '''
#     This function will utilize the fitted spline to calculate the coeffecient of friction for a given normal load

#     Inputs:
#     'forceNormal' - Type: Float 

#     Outputs:
#     'muEff' - Type: Float
#     '''
#     max_lateral_force = []
#     slip_angles_eval = np.linspace(-.2, .2, 100)
#     for angle in slip_angles_eval:
#             # Predict lateral force using the fitted model
#             X_pred = poly.transform([[angle, forceNormal]])
#             lateral_force_pred = regressor.predict(X_pred)[0]
            
#             # Append lateral force and corresponding normal force
#             max_lateral_force.append(abs(lateral_force_pred))
#     muEff = max(max_lateral_force)/forceNormal

#     return muEff
##### SHIT ABOVE IS ASS AND TOO HARD TO IMPLEMENT BOOOOOOOOO WOMP
### USE BELOW TO CALCULATE THE LATERAL FORCE 
    
# for angle in slip_angles_eval:
#         # Predict lateral force using the fitted model
#         X_pred = poly.transform([[angle, force]])
#         lateral_force_pred = regressor.predict(X_pred)[0]
        
#         # Append lateral force and corresponding normal force
#         max_lateral_force.append(abs(lateral_force_pred))
# muEff = max(max_lateral_force)/force

def calculateMu(force):

    return func(force)   
####
print(calculateMu(1000))