import random
import copy

class Location():
    
    def __init__(self, locationName):
        self.location = locationName
        # Actions are keys, values are list of tuples. Tuples have the destination and then probability
        self.actionDict = {}
        #Set up the same way but has a value associated with each, all 0 at the moment
        self.actionValue = {}
        # Used for determining which action, assigns ints to an action
        self.probRanges = {}
        #Keeps track of where the ball goes next
        self.nextLocation = {}
        # Keeps scores for a specific choice
        self.choiceScores = {}
        # Keeps a record of the actions it has done itself to develop the model
        self.actionsDone= []
        #Initial value zero
        self.positionValue = 0
        # So that all values can update first, save last value
        self.previousValue = 0
        self.bestAction = ""
        self.actionCount = 0
        
        # Adds the action to the appropriate dictionaries
    def addAction(self, action, destination, probablilty):
        dest = (destination, probablilty)
        if action not in self.actionDict.keys():
            self.actionDict[action] = [dest]
            self.actionValue[action] = [(destination, 0)]
        else:
            self.actionDict[action].append(dest)
            self.actionValue[action].append((destination, 0))
            
      
    # For deciding randomly which result, returns the result
    def getRandomResult(self, givenAction):
        number = random.randint(0, 99)
        # If this action has not occurred, create the offset
        if givenAction not in self.probRanges.keys():
            offset = 0
            ranges  = [0]
            for destTuple in self.actionDict[givenAction]:
                percentage = float(destTuple[1]) * 100
                percentage = int(percentage)
                ranges.append(percentage + offset)
                offset += percentage
            self.probRanges[givenAction] = ranges
        else:
            ranges = self.probRanges[givenAction]
        # The i index of the ranges correlates to the i index of the action performed
        for i in range(len(ranges) - 1):
            if number in range(ranges[i], ranges[i+1]):
                return self.actionDict[givenAction][i][0]
        
    # Performs an action, a random one if none is given
    def performAction(self, newAction = ''):
        if len(newAction) == 0:
            randomIndex = random.randint(0, len(self.actionDict.keys())-1)
            newAction = list(self.actionDict.keys())[randomIndex]
        result = self.getRandomResult(newAction)
        if newAction not in self.nextLocation.keys():
            self.nextLocation[newAction] = [(result, 1)]
        else :
            traveledTo = []
            for tuplePairs in self.nextLocation[newAction]:
                traveledTo.append(tuplePairs[0])
            if result not in traveledTo:
                self.nextLocation[newAction].append((result, 1))
            else:
                tupleIndex = 0
                for i in range(len(self.nextLocation[newAction])):
                    if self.nextLocation[newAction][i][0] == result:
                        tupleIndex = i
                        break
                old = self.nextLocation[newAction][i]
                new = (old[0], old[1]+1)
                self.nextLocation[newAction][i] = new
        if newAction not in self.actionsDone:
            self.actionsDone.append(newAction)
        self.actionCount +=1
        return result
    
    def calculateValues(self, gamma):
        connectedTo = []
        for usedActions in self.nextLocation.keys():
            for place in self.nextLocation[usedActions]:
                if place[0] not in connectedTo:
                    connectedTo.append(place[0])
        # actionsPerformed and these two should have same indexing
        actionsAndCosts = {}
        # After executing, all action paths should have a cost associated
        for testAction in self.actionsDone:
            # The constant minus for the cost of moving
            actionTotal = -0.04
            for pairing in self.nextLocation[testAction]:
                nearby = pairing[0]
                count = pairing[1]
                probability = count/self.actionCount
                if nearby == "In":
                    subtotal = gamma * probability * 1
                    actionTotal += subtotal
                else:
                    nearbyObj = locationList[nearby]
                    subtotal = gamma * probability * nearbyObj.previousValue
                    actionTotal += subtotal
            actionsAndCosts[testAction] = actionTotal
        
        highestAction = [list(actionsAndCosts.keys())][0][0]
        highestValue = actionsAndCosts[highestAction]
        for actionKey in actionsAndCosts.keys():
            if actionsAndCosts[actionKey] > highestValue:
                highestAction = actionKey
                highestValue = actionsAndCosts[actionKey]
        self.previousValue = self.positionValue
        self.positionValue = highestValue
        self.bestAction = highestAction
        return actionsAndCosts
        
        
    #For printing out the values and the probability
    def printOut(self, gamma):
        printString = self.location
        #for cycling through thw possible actions
        for actionString in self.actionDict.keys():
            substring = "/" + actionString
            #Cycle through destinations, will find probablitlity 
            for countPairing in self.nextLocation[actionString]:
                destString = countPairing[0]
                count = countPairing[1]
                probability = count/self.actionCount
                actionsAndCosts = self.calculateValues(gamma)
                print(printString + substring + '/' + destString + " " + str(probability))
        
                
    
    # Calls itself until a path to the goal is found, method will be random or model
def modelBasedRecursive(currentLocation, method):
    if method == "random":
        result = currentLocation.performAction()
    else:
        result = currentLocation.performAction(currentLocation.bestAction)
        
    if result != "In":
        modelBasedRecursive(locationList[result], method)
    
    
      
# The base driver code of the model based experiment      
def modelBased(gamma, epsilon):
    firstLocation = locationList[list(locationList.keys())[0]]
    modelBasedRecursive(firstLocation, "random")
    for locationObj in locationList.values():
        if locationObj.actionCount != 0:
           locationObj.calculateValues(gamma)
    count = 1
    while count < 1001:
        chance = random.randint(0, 99)
        if chance < epsilon * 100:
            modelBasedRecursive(firstLocation, "random")
            for locationObj in locationList.values():
                if locationObj.actionCount != 0:
                    locationObj.calculateValues(gamma)
        else:
            modelBasedRecursive(firstLocation, "model")
            for locationObj in locationList.values():
                if locationObj.actionCount != 0:
                    locationObj.calculateValues(gamma)
        count += 1
    for locationObj in locationList.values():
        locationObj.printOut(gamma)
    

#Will change to standard input, had it this way as it was easier
file = open("assignment2test.txt", "r")
#dictionary of locations, keys are the location name, values are the object
locationList = {}
for line in file:
    line = line.strip('\n')
    location, action, destination, prob = line.split("/")
    if location not in locationList.keys():
        locationList[location] = Location(location)
        locationList[location].addAction(action, destination, prob)
    else:
        locationList[location].addAction(action, destination, prob)
locationBackup = copy.deepcopy(locationList)
print("High gamma, low epsilon")
modelBased(0.9, 0.1)
print()
locationList = locationBackup
locationBackup = copy.deepcopy(locationList)
print("Low gamma, low epsilon")
modelBased(0.2,0.1)
print()
locationList = locationBackup
locationBackup = copy.deepcopy(locationList)
print("High gamma, high epsilon")
modelBased(0.9,0.9)
print()
locationList = locationBackup
locationBackup = copy.deepcopy(locationList)
print("Low gamma, high epsilon")
modelBased(0.2,0.9)
