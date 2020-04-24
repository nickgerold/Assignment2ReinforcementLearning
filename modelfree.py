import random
import copy

#Using utility = Reward + gamma*P(s) U(s')

def modelFreeLearning(explore, discount, actionStates, utilityScore):
    currentState = "Fairway"
    finalState = "In"
    nextState = ""
    par = 4
    stroke = 1
    endState = False

    while currentState != finalState or endState == True:
        #If stroke count gets above par, start to exploit rather than explore
        if stroke > par:
            explore = 0.3
        actionDecider = random.random() #random value to decide whether to explore or to exploit
        nextActions = []

        #Choosing to either explore or exploit
        if actionDecider < explore: #to explore
            nextActions = list(actionStates[currentState].keys())
            randomAction = random.choice(nextActions)
            currentAction = randomAction
        else: #to exploit
           nextActions = list(actionStates[currenState].keys())
           randomAction = random.choice(nextActions)
           if utility[currentState][randomAction] >= 1:
               currentAction = randomAction
           else:
                currentAction = random.choice(nextActions)

        #Getting the next location from the action committed
        possibleNewLocation = actionStates[currentState][currerntAction]
        locationDecider = random.random()
        for location in possibleNewLocation:
            locationInt = locationInt + possibleNewLocation[location]
            if locationDecider < locationInt:
                nextState = location
        currentReward = 0

        #Calculating Reward (1 for in, 0 for rest) 
        if nextState == "In":
            currentReward = 1 / (stroke / par) #if the going for eagle/birdies the reward is greater due to more gain
        else:
            currentReward = 0 #no reward for hitting it close as golf is a 0/1 style game. Its in or out.
        successorUtility = 0

        #Calculating utility score using bellmans equation
        for actions in utility[nextState]:
            if utility[nextState][actions] > successorUtility:
                successorUtility = utility[nextState][actions]
        utility[currentState][currentAction] = utility[currentState][currentAction] + currentReward + discount * (successorUtility)
        currentState = nextState

        #Fail safe to stop while loop in case spaghetti code happens
        if currentState == "In":
            endState = True

    #Printing out the triplet
    for location in utility:
        for action in utility[location]:
            print(location, action, utility[location][action])

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
    explorationRate = 0.7 #epsilon
    discountValue = 0.9 #gamma
    actionStatesBackup = copy.deepcopy(actionStates) #backup actionStates dict for further use
    utility = {} #contains locations, actions, utility
    for location in actionStates:
        utility[location] = {}
        for action in actionStates[location]:
            utility[location][action] = 1
    modelFreeLearning(explorationRate, discountValue, actionStates, utility)

if __name__ == '__main__':
    __main__()

