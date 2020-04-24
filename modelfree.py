import random
import copy

#Using utility = Reward + gamma*P(s) U(s')

def modelFreeLearning(explore, discount, learn, actionStates, utilityScore):
    currentState = "Fairway"
    finalState = "In"
    nextState = ""

    while currentState != finalState:
        actionDecider = random.random() #random value to decide whether to explore or to exploit
        nextActions = []
        if actionDecider < explore: #to explore
            nextActions = list(actionStates[currentState].keys())
            randomAction = random.choice(nextActions)
            currentAction = randomAction
        else: #to exploit
            #do that
            num = random.random()
        possibleNewLocation = actionStates[currentState][currerntAction]
        locationDecider = random.random()
        for location in possibleNewLocation:
            locationInt = locationInt + possibleNewLocation[location]
            if locationDecider < locationInt:
                nextState = location



def __main__():
    #Will change to standard input, had it this way as it was easier
    file = open("assignment2test.txt", "r")
    actionStates = {}   #actionStates is the final dictionary used in the modelFreeLearning
    for line in file:
        actionLocationProb = line.split("/") #get the locations, actions, probabilities from the text file
        if actionLocationProb[0] not in actionStates:
            actionStates[actionLocationProb[0]] = {} #locations
        if actionLocationProb[1] not in actionStates[actionLocationProb[0]]:
           actionStates[actionLocationProb[0]][actionLocationProb[1]] ={}
        actionStates[actionLocationProb[0]][actionLocationProb[1]][actionLocationProb[2]] = float(actionLocationProb[3].rstrip()) #use R strip to remove white spaces on right hand side 
    explorationRate = 0.5 #epsilon
    learningRate = 0.1 #RL
    discountValue = 0.9 #gamma
    actionStatesBackup = copy.deepcopy(actionStates) #backup actionStates dict for further use
    utility = {} #contains locations, actions, utility
    for location in actionStates:
        utility[location] = {}
        for action in actionStates[location]:
            utilility[location][action] = 1
    modelFreeLearning(explorationRate, discountValue, learningRate, actionStates, utility)

if __name__ == '__main__':
    __main__()
