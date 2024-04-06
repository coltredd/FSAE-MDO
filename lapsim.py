import tireModel
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

def timeThrottleCalc(vEntry,power,vMaxAllowed):
    
    # import as needed


    # determine if power or traction limited


    # 

    return timeThrottle 

def timeBrakeCalc(vEntry,vCorner):

    # max possible deceleration

    # calculate load under braking
