class vehicleDynamics:

    def __init__(self,track,wheelBase,cgHeight):
        self.track = track
        self.wheelbase = wheelBase
        self.cgHeight = cgHeight
        self.lapTime = 0

    def timeCornerCalc(speedEntry,radius,angle):
        '''
        Function will calculate the time it take to go through a corner

        Inputs:
        'speedEntry'
        Speed Entry to the track formation. This case its the corner entry speed. Equal to speed at end of braking
        Type: Float 
        Units: m/s

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

        # calculate max velocity around corner using derived equations

        vMax = (muEff*radius)**(1/2)

        # Calculate time to go around corner

        timeCorner = (3.14159265*radius)*(angle/180)/vMax

        return timeCorner

    def timeAccel(speedEntry)