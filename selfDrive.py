import operator

def main():
    Features, ridedata = parseData("c_no_hurry.in")
    rides = []
    i = 0
    for ride in ridedata:
        rides.append(Ride(ride, i))
        i += 1
    drivers = []
    i =0
    for i in range(int(Features[2])):
        drivers.append(Driver(i,0,0))
        i += 1
    moving(drivers,rides)

def parseData(filename):
    f= open(filename, "r")
    f = f.read().split("\n")
    KeyFeatures = f[0].split()
    rides = []
    for row in range(int(KeyFeatures[3])):
        rides.append(f[row+1].split())
    return KeyFeatures, rides

def sortRides(rides,attr ):
    return sorted(rides,key=operator.attrgetter(attr))



class Ride:
    def __init__(self,data, ident):
        self.startTime = int(data[4])
        self.endTime = int(data[5])
        self.xStart = int(data[0])
        self.yStart = int(data[1])
        self.xFinish = int(data[2])
        self.yFinish = int(data[3])
        self.rideIdent = int(ident)
        self.MinSteps = int(self.numSteps())
        self.lateStart = int(self.latestStart())
        self.claimed = False

    def numSteps(self):
        return (abs(self.xStart - self.xFinish) + abs(self.yStart - self.yFinish))

    def timeBeforeExpire(self, currentTime):
        return self.lateStart - currentTime

    def latestStart(self):
        time = self.endTime - self.MinSteps
        if time >= self.startTime:
            return time
        else:
            return -1
class Driver:
    def __init__(self,ref,x,y):
        self.uRef = ref
        self.x = x
        self.y = y
        self.intendedX = 0
        self.intendedY = 0
        self.stepsTaken = 0
        self.claimedRide = -1
        self.pickedUp = False
        self.ride = Ride
        self.outputLine =[]

    def forceMove(self,Location): # force the driver to a location without taking steps
        self.x = Location[0]
        self.y = Location[1]

    def takeStep(self): #move the driver to its intended place
        if self.x != self.intendedX:
            if self.x > self.intendedX:
                self.x -= 1
            else:
                self.x += 1
            self.stepsTaken += 1
        elif self.y!= self.intendedY:
            if self.y > self.intendedY:
                self.y -= 1
            else:
                self.y += 1
            self.stepsTaken += 1
        elif (self.x == self.intendedX) and (self.y == self.intendedY):
            if (self.pickedUp == False and self.claimedRide != -1):
                self.setFinish()
            elif (self.pickedUp ==True and self.claimedRide != -1):
                self.finishRide()


    def claimRide(self,ride):
        ride.claimed = True
        self.claimedRide = ride.rideIdent
        self.intendedX = ride.xStart
        self.intendedY = ride.yStart
        self.ride = ride

    def setFinish(self):
        self.intendedX = self.ride.xFinish
        self.intendedY = self.ride.yFinish
        self.pickedUp = True

    def finishRide(self):
        self.addOutputLine()
        self.claimedRide = -1

    def addOutputLine(self):
        self.outputLine.append(self.ride.rideIdent)

    def getOutputLine(self):
        length = len(self.outputLine)
        message = str(length)
        for i in self.outputLine:
            message += " " + str(i)
        return message

def numStepsAB(locationA,locationB):
    return (abs(locationA[0] - locationB[0]) + abs(locationA[1] - locationB[1]))

def removeUndoable(drivers, rides,currentTime):
    canDo = []
    for ride in rides:
        possible =False
        for driver in drivers:
            if possible == False:
                if numStepsAB([driver.x,driver.y],[ride.xStart,ride.yStart])+ currentTime <=ride.lateStart:
                    possible =True
        if possible == True:
            canDo.append(ride)
    return canDo

def moving(drivers,rides):
    notFinished = True
    time = 0
    while notFinished:
        rides = removeUndoable(drivers,rides,time)
        rides = sortRides(rides, 'lateStart')
        for driver in drivers:
            if driver.claimedRide == -1:
                length = len(rides)
                escapeClause = False
                i =0
                while driver.claimedRide == -1 and not(escapeClause)and len(rides) != 0:
                    if rides[i].claimed == False and (numStepsAB([driver.x,driver.y],[rides[i].xStart,rides[i].yStart])+time<= rides[i].lateStart):
                        driver.claimRide(rides[i])
                        rides[i].claimed = True
                    i+= 1
                    if i >= length-1:
                        escapeClause = True
            # for driver in drivers:
            #     print driver.claimedRide
            driver.takeStep()
        time += 1
        if len(rides)== 0:
            notFinished = False
    saveFile = open("c.txt","w+")
    message = ""
    for driver in drivers:
        message += driver.getOutputLine()+ "\n"
    saveFile.write(message)
main()
