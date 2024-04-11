from tireModel import calculateMu
def timeCornerCalc(radius,angle):
    '''
    Function will calculate the time it take to go through a corner

    Inputs:

    'radius'
    The radius of the turn
    Type: Float
    Units: m

    'angle'
    The angular duration of the turn
    Type: Float
    Units: degrees

    Outputs:
    'timeCorner'
    Time it takes to go through corner with given inputs
    Type: Float
    Units: s

    '''
    
    # Calcuklate load transfer in corner. SHould be entire lateral load transfer. Load for all wheels

    
    # Find maximum normal load tire. This will result in the lowest grip available without having to call calculateMu and waste run time
    maxLoad = max(loads)

    muEff = calculateMu(maxLoad)
    # calculate max velocity around corner using derived equations

    vMax = (muEff*radius)**(1/2)

    # Calculate time to go around corner

    timeCorner = (3.14159265*radius)*(angle/180)/vMax

    return timeCorner

def timeStrightCalc(vEntry,vMaxAllowed,params):
    
    # import as needed

    # break apart params dictionary

    cgZ = params['CG'][2]
    wheelbase = params['wheelbase']
    cgX = params['CG'][0]
    mass = params['mass']
    straightLength = params['track']['straight']

    # calculate max accel 

    vMax = vMaxAllowed / 2.237  # maxV from mph to m/s
    # powerHp = 65
    # gravity = 9.81
    # powerWatts = powerHp * 745.7 # watts
    # accelPowerLimit = (powerWatts / mass) * (vMax - vEntry) / (vMax**2 - vEntry**2)  # max accel in m/s^2 POWER LIMIT


    ## accel but with torque

    torque = 30 *1.35582 # Nm
    wheelRadius = (8/12) *.0254 ## m
    accelPowerLimit = (torque/wheelRadius)/mass

    # calculate loads on rear tires

    rearLoad = (mass/wheelbase)*(gravity*(wheelbase-cgX)+(accelPowerLimit*cgZ))
    rearLoadTire = rearLoad / 2
    muPowerLimit = calculateMu(rearLoadTire) ## designated as mu for power limited case

    # calculate load on tire for max accel without tire lift

    # solve for accel such that frontLoad = 0 

    tol = 1e-6
    check = 1
    iter = 0
    accelGuess = 1.2*gravity
    maxIter = 1e4
    while (check > tol) and (iter<maxIter):
    
        # calculate horizontal force by tires from guess accel
    
        rearLoad = (mass/wheelbase)*(gravity*(wheelbase-X)+(accelGuess*cgZ))
        rearLoadTire = rearLoad/2
        muDerive = calculateMu(rearLoadTire)*0.95
        
        forceTraction = muDerive*rearLoad
        accelDerive = (forceTraction)/mass        
        error = accelDerive - accelGuess
        check = abs(error)
        accelGuess += accelDerive *error
        
        iter += 1   

    accelGripLimit = accelGuess


    if accelGripLimit < accelPowerLimit:
        accelMaster = accelGripLimit
    else:
        accelMaster = accelPowerLimit

    # calculate distance traveled to go from corner exit to max speed

    deltaXThrottle = (vMax**2 - vEntry**2)/(2*accelMaster)

    # calcualte time on throttle
    timeThrottle = (vMax-vEntry)/accelMaster
    # brake calcualtions 


    tol = 1e-6
    check = 1
    iter = 0
    deccelGuess = 1.2*gravity
    maxIter = 1e4
    while (check > tol) and (iter<maxIter):
    
        # calculate horizontal force by tires from guess accel
    
        rearLoad = (mass/wheelbase)*(gravity*(wheelbase-X)+(accelGuess*cgZ))
        frontLoad = mass*gravity - rearLoad
        frontLoadTire = frontLoad/2
        muDerive = calculateMu(frontLoadTire)*0.95
        
        forceTraction = muDerive*rearLoad
        deccelDerive = (forceTraction)/mass        
        error = deccelDerive - deccelGuess
        check = abs(error)
        deccelGuess += deccelDerive *error
        
        iter += 1 

    deccelMaster = deccelGuess

    # calcualte distance and time to brake

    deltaXBrake = (vMax**2 - vEntry**2)/(2*deccelMaster)

    timeBrake = (vMax-vEntry)/deccelMaster

    # calculate time spent at max speed

    distanceLimiter = straightLength - (deltaXThrottle + deltaXBrake)

    timeLimiter = distanceLimiter/vMax


    # put it all together 


    timeStright = timeThrottle + timeBrake + timeLimiter


    return timeStraight 

