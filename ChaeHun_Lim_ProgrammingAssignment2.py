import random
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
#---------------------INSTRUCTIONS--------------

#pip install matplotlib and numpy if your system do not have them.
#There are inputs that you can change below to adjust the game
#in the bottom of the main function, there are functions for printing graphs for each condition
#make sure you read what each print function does to get the desired graph of your need


#------------------Class Declaration----------------------------
class Player:
    def __init__(self, identity, id, decision, enemies, score):
        self.identity = identity
        self.id = id
        self.decision = decision
        self.enemies = enemies
        self.score = score

class T4t(Player):
    def __init__(self, identity, id, decision, enemies, score):
        super().__init__(identity, id,decision,enemies, score)
class Grudger(Player):
    def __init__(self, identity, id, decision, enemies, score):
        super().__init__(identity,id,decision,enemies, score)
class Ac(Player):
    def __init__(self,identity, id, decision, enemies, score):
        super().__init__(identity,id,decision,enemies, score)
class Ad(Player):
    def __init__(self, identity, id, decision, enemies, score):
        super().__init__(identity, id,decision,enemies, score)
#----------------------CHANGE INPUTS HERE---------------------
n = 100 #number of players
k = 20  #number of generations
m = 5   #number of games in each generation
p = 5   #percentage of players survived, removed from the game
delta = 5 #delta to adjust p for every generation played p = p +- delta
firstPlayer = "t4t" #first type of the player
secondPlayer = "grudger" #second type of the player
thirdPlayer = "ac"#third type of the player
fourthPlayer = "ad"#last type of the player
#--------------INITIALIZED VARIABLES-----------------------


generation = {}
enemies = {}
shuffledGen = {}
sortedHelper = {}
sortingHelper = {}
numGrudger = 0
numAc = 0
numAd = 0
numT4t = 0
scoreG = 0
scoreAc = 0
scoreAd = 0
scoreT = 0
sumS = 0


#----------------------Bar Graph Variables---------------
label = []
for i in range(0,k):
    label.append("Generation " + str(i + 1))
perData = []
perDataG= []
perDataT= []
perDataAc= []
perDataAd= []
avgData = []
avgDataG = []
avgDataT = []
avgDataAc = []
avgDataAd = []

totTypeData =[]
totAc = []
totAd = []
totT = []
totG = []
totData = []
allData = []

pData = []

lastAvg = []
lastPer = []
lastTot = []
lastTotAll =[]

#------------------------FUNCTIONS----------------------

#initialize generations
def initGen():
    for i in range(0, n-1, 4):
        enemies1 = []
        enemies2 = []
        enemies3 = []
        enemies4 = []
        #initilize enemy array
        for j in range(0, n):
            enemies1.append(j)
            enemies2.append(j)
            enemies3.append(j)
            enemies4.append(j)


        random.shuffle(enemies1)
        random.shuffle(enemies2)
        random.shuffle(enemies3)
        random.shuffle(enemies4)
        firstDecision = True
        secondDecision = True
        thirdDecision = True
        fourthDecision = True
        if firstPlayer == "ad":
            firstDecision = False
        if secondPlayer == "ad":
            secondDecision = False
        if thirdPlayer == "ad":
            thirdDecision = False
        if fourthPlayer == "ad":
            fourthDecision = False
        T4t_init = T4t(firstPlayer,i, firstDecision, enemies1, 0)
        Grudger_init = Grudger(secondPlayer, i+1, secondDecision, enemies2,0 )
        Ac_init = Ac(thirdPlayer, i+2, thirdDecision, enemies3, 0)
        Ad_init = Ad(fourthPlayer, i+3, fourthDecision, enemies4, 0)
        generation[i] = T4t_init
        generation[i+1] = Grudger_init
        generation[i+2] = Ac_init
        generation[i+3] = Ad_init

#randomize the list
def shuffleList():
    keys = list(generation.keys())
    random.shuffle(keys)

    for key in keys:
      shuffledGen.update({key:generation[key]})

#play the game for m times for every player vs its enemy
def play():
    for player in shuffledGen.values():

        for enemy in player.enemies:
            if (player.identity == "grudger" or player.identity == "t4t"):
                player.decision = True
            if (shuffledGen[enemy].identity == "grudger" or shuffledGen[enemy].identity == "t4t"):
                shuffledGen[enemy].decision = True


            if(enemy != player.id): #check if enemy isn't the player itself
                for h in range(0,m):

                    if(player.decision == True and shuffledGen[enemy].decision == True):
                         player.score += 3
                         shuffledGen[enemy].score += 3
                         if (player.identity == "t4t"):
                             player.decision = True

                    elif(player.decision == True and shuffledGen[enemy].decision == False):
                         player.score += 0
                         shuffledGen[enemy].score += 5
                         if (player.identity == "grudger"):
                             player.decision = False

                         if (player.identity == "t4t") :
                             player.decision = False
                         if (shuffledGen[enemy].identity == "t4t") :
                             shuffledGen[enemy].decision = True
                    elif (player.decision == False and shuffledGen[enemy].decision == True):
                        player.score += 5
                        shuffledGen[enemy].score += 0
                        if (player.identity == "t4t"):
                            player.decision = True
                        if (shuffledGen[enemy].identity == "t4t" or shuffledGen[enemy].identity == "grudger" ):
                            shuffledGen[enemy].decision = False
                    elif (player.decision == False and shuffledGen[enemy].decision == False):
                        player.score += 1
                        shuffledGen[enemy].score += 1
                        if (player.identity == "t4t"):
                            player.decision = False



                if player.id in shuffledGen[enemy].enemies:

                   shuffledGen[enemy].enemies.remove(player.id)


#update list after every game has played based on p
def updateList():
    rand = random.randint((-1*delta),delta)
    updatedP = p + rand
    percentage = updatedP * 0.01 * n
    castedPer = int(percentage)
    pData.append(updatedP)


    li = list(sortedHelper.items())
    originalLi = list(shuffledGen.items())
    listSurvived = []


    for x in range(0, castedPer):

        survivedId = li[x][0]

        listSurvived.append(shuffledGen.get(survivedId))
        last = n - x - 1
        lowest = li[last]
        shuffledGen.pop(lowest[0])

        pl  = shuffledGen.get(survivedId)
        identity = pl.identity
        decision = shuffledGen.get(survivedId).decision
        enem = shuffledGen.get(survivedId).enemies


        newPlayer = Player(identity,lowest[0],decision,enem,pl.score)
        shuffledGen.update({lowest[0]: newPlayer})


    for player in shuffledGen.values():
        player.score = 0
        player.enemies.clear()
        for j in range(0, n):

           player.enemies.append(j)

def sumScore():
    global scoreG,scoreT,scoreAc,scoreAd

    for player in shuffledGen.values():

        if player.identity == "grudger":
            scoreG += player.score


        if player.identity == "t4t":
            scoreT += player.score
        if player.identity == "ac":
            scoreAc += player.score

        if player.identity == "ad":
            scoreAd += player.score



def count():
        global numAd
        global numAc
        global numGrudger
        global numT4t
        for player in shuffledGen.values():
            if player.identity == "grudger":
               numGrudger += 1


            if player.identity == "t4t":
                numT4t += 1
            if player.identity == "ac":
                numAc += 1
            if player.identity == "ad":
                numAd += 1
#prints a graph of percentage of each type of players
def printPerGraph():
    plt.rcParams["figure.figsize"] = (20, 4)
    fig, ax = plt.subplots()
    index = np.arange(k)
    barW = 0.2
    opacity = 1
    for i in range(0, k):
        if i == 0:
            rect = plt.bar(index, perData[0], barW, alpha=opacity, color='b', label='Grudger')
            rect1 = plt.bar(index + (barW), perData[1], barW, alpha=opacity, color='g', label='T4T')
            rect2 = plt.bar(index + (2 * barW), perData[2], barW, alpha=opacity, color='r', label='AC')
            rect3 = plt.bar(index + (3 * barW), perData[3], barW, alpha=opacity, color='y', label='AD')
        else:
            rect = plt.bar(index, perData[0], barW, alpha=opacity, color='b')
            rect1 = plt.bar(index + (barW), perData[1], barW, alpha=opacity, color='g')
            rect2 = plt.bar(index + (2 * barW), perData[2], barW, alpha=opacity, color='r')
            rect3 = plt.bar(index + (3 * barW), perData[3], barW, alpha=opacity, color='y')

    plt.xlabel('Generation')
    plt.ylabel('Percentage')
    plt.title('Percentage by Generation')
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of average payoff of each type of players
def printAvgGraph():
    plt.rcParams["figure.figsize"] = (25, 6)
    fig, ax = plt.subplots()
    index = np.arange(k)
    barW = 0.2
    opacity = 1
    for i in range(0, k):
        if i == 0:
            rect = plt.bar(index, avgData[0], barW, alpha=opacity, color='b', label='Grudger')
            rect1 = plt.bar(index + (barW), avgData[1], barW, alpha=opacity, color='g', label='T4T')
            rect2 = plt.bar(index + (2 * barW), avgData[2], barW, alpha=opacity, color='r', label='AC')
            rect3 = plt.bar(index + (3 * barW), avgData[3], barW, alpha=opacity, color='y', label='AD')
        else:
            rect = plt.bar(index, avgData[0], barW, alpha=opacity, color='b')
            rect1 = plt.bar(index + (barW), avgData[1], barW, alpha=opacity, color='g')
            rect2 = plt.bar(index + (2 * barW), avgData[2], barW, alpha=opacity, color='r')
            rect3 = plt.bar(index + (3 * barW), avgData[3], barW, alpha=opacity, color='y')

    plt.xlabel('Generation')
    plt.ylabel('Average Payoff')
    plt.title('Average Payoff  by Generation')
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of average payoff of each type of players varied by p
def printAvgGraphP():
    plt.rcParams["figure.figsize"] = (25, 6)
    fig, ax = plt.subplots()
    index = np.arange(1)
    barW = 0.2
    opacity = 1

    rect = plt.bar(index,lastAvg[0] , barW, alpha=opacity, color='b', label='Grudger')
    rect1 = plt.bar(index + (barW), lastAvg[1], barW, alpha=opacity, color='g', label='T4T')
    rect2 = plt.bar(index + (2 * barW), lastAvg[2], barW, alpha=opacity, color='r', label='AC')
    rect3 = plt.bar(index + (3 * barW), lastAvg[3], barW, alpha=opacity, color='y', label='AD')
           # rect4 = plt.bar(index + (4 * barW), pData, barW, alpha=opacity, color='purple', label='P-val')


    plt.xlabel('Generation')
    plt.ylabel('Average Payoff')
    plt.title('Average Payoff (P-varied)  P = ' + str(pData[k-1]))
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of percentage of each type of players varied by p
def printPerGraphP():
    plt.rcParams["figure.figsize"] = (25, 6)
    fig, ax = plt.subplots()
    index = np.arange(1)
    barW = 0.2
    opacity = 1

    rect = plt.bar(index,lastPer[0] , barW, alpha=opacity, color='b', label='Grudger')
    rect1 = plt.bar(index + (barW), lastPer[1], barW, alpha=opacity, color='g', label='T4T')
    rect2 = plt.bar(index + (2 * barW), lastPer[2], barW, alpha=opacity, color='r', label='AC')
    rect3 = plt.bar(index + (3 * barW), lastPer[3], barW, alpha=opacity, color='y', label='AD')
           # rect4 = plt.bar(index + (4 * barW), pData, barW, alpha=opacity, color='purple', label='P-val')


    plt.xlabel('Generation')
    plt.ylabel('Percentage')
    plt.title('Percentage of population (P-varied)  P = ' + str(pData[k-1]))
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of total payoff of each type of players varied by p
def printTotGraphP():
    plt.rcParams["figure.figsize"] = (25, 6)
    fig, ax = plt.subplots()
    index = np.arange(1)
    barW = 0.2
    opacity = 1

    rect = plt.bar(index,lastTot[0] , barW, alpha=opacity, color='b', label='Grudger')
    rect1 = plt.bar(index + (barW), lastTot[1], barW, alpha=opacity, color='g', label='T4T')
    rect2 = plt.bar(index + (2 * barW), lastTot[2], barW, alpha=opacity, color='r', label='AC')
    rect3 = plt.bar(index + (3 * barW), lastTot[3], barW, alpha=opacity, color='y', label='AD')



    plt.xlabel('Generation')
    plt.ylabel('Total Payoff')
    plt.title('Total Payoff of population (Group, P-varied)  P = ' + str(pData[k-1]))
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of combined payoff of each type of players varied by p
def printTotAllGraphP():
    plt.rcParams["figure.figsize"] = (25, 6)
    fig, ax = plt.subplots()
    index = np.arange(1)
    barW = 0.2
    opacity = 1

    rect = plt.bar(index,lastTotAll , barW, alpha=opacity, color='b')




    plt.xlabel('Generation')
    plt.ylabel('Total Payoff')
    plt.title('Total Payoff of population (Combined, P-varied)  P = ' + str(pData[k-1]))
    plt.legend()
    plt.xticks(index, (
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints a graph of total payoff of each type of players
def printTotGraph():
    plt.rcParams["figure.figsize"] = (20, 4)
    fig, ax = plt.subplots()
    index = np.arange(k)
    barW = 0.2
    opacity = 1
    for i in range(0, k):
        if i == 0:
            rect = plt.bar(index, totData[0], barW, alpha=opacity, color='b', label='Grudger')
            rect1 = plt.bar(index + (barW), totData[1], barW, alpha=opacity, color='g', label='T4T')
            rect2 = plt.bar(index + (2 * barW), totData[2], barW, alpha=opacity, color='r', label='AC')
            rect3 = plt.bar(index + (3 * barW), totData[3], barW, alpha=opacity, color='y', label='AD')
        else:
            rect = plt.bar(index, totData[0], barW, alpha=opacity, color='b')
            rect1 = plt.bar(index + (barW), totData[1], barW, alpha=opacity, color='g')
            rect2 = plt.bar(index + (2 * barW), totData[2], barW, alpha=opacity, color='r')
            rect3 = plt.bar(index + (3 * barW), totData[3], barW, alpha=opacity, color='y')

    plt.xlabel('Generation')
    plt.ylabel('Total Payoff')
    plt.title('Total Payoff  by Generation (Group)')
    plt.legend()
    plt.xticks(index, (
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()
#prints total graph of combined payoff of every type of players
def printTotGraphAll():
    plt.rcParams["figure.figsize"] = (20, 4)
    fig, ax = plt.subplots()
    index = np.arange(k)
    barW = 0.2
    opacity = 1
    for i in range(0, k):

            rect = plt.bar(index, allData, barW, alpha=opacity, color='b')


    plt.xlabel('Generation')
    plt.ylabel('Total Payoff')
    plt.title('Total Payoff  by Generation (Combined)')
    plt.legend()
    plt.xticks(index, (
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))

    plt.show()

#main function
if __name__ == "__main__":
    initGen()
    shuffleList()

    for round in range (0,k):

        play()
        for player in shuffledGen.values():
            sortingHelper[player.id] = player.score
        sortedHelper = OrderedDict(sorted(sortingHelper.items(), key=lambda x: x[1], reverse=True))

        count()
        print("PERCENTAGE: ", "Gen", round + 1, ": ", "G: ", numGrudger / n * 100, "%", "T4T: ", numT4t / n * 100, "%", "AC: ",
              numAc / n * 100, "%", "AD: ", numAd / n * 100, " %")
        perDataAc.append(numAc/n)
        perDataT.append(numT4t/n)
        perDataAd.append(numAd/n)
        perDataG.append(numGrudger/n)


        sumScore()
        sumS =  scoreT + scoreG + scoreAd + scoreAc
        print("SCORE: ", "Gen", round + 1, ": ", "G: ", scoreG,  "T4T: ", scoreT,  "AC: ",
             scoreAc,  "AD: ", scoreAd, "SUM SCORE: ", sumS)
        allData.append(sumS)
        totG.append(scoreG)
        totT.append(scoreT)
        totAc.append(scoreAc)
        totAd.append(scoreAd)
        avgAc = 0
        avgAd = 0
        avgG = 0
        avgT = 0
        if numAc != 0:
            avgAc = scoreAc/numAc
        if numAd != 0:
            avgAd = scoreAd / numAd
        if numT4t != 0:
            avgT = scoreT / numT4t
        if numGrudger != 0:
            avgG = scoreG / numGrudger
        print("AVG SCORE: ", "Gen", round + 1, ": ", "G: ", scoreG, "T4T: ", scoreT, "AC: ",
              scoreAc, "AD: ", scoreAd)

        avgDataAc.append(avgAc)
        avgDataAd.append(avgAd)
        avgDataT.append(avgT)
        avgDataG.append(avgG)
        scoreT = 0
        scoreAd = 0
        scoreG = 0
        scoreAc = 0
        sumS = 0
        numAc = 0
        numAd = 0
        numT4t = 0
        numGrudger = 0
        realP = p
        updateList()
        p = realP
    lastAvg.append(avgDataG[k-1])
    lastAvg.append(avgDataT[k-1])
    lastAvg.append(avgDataAc[k-1])
    lastAvg.append(avgDataAd[k-1])
    lastPer.append(perDataG[k-1])
    lastPer.append(perDataT[k - 1])
    lastPer.append(perDataAc[k - 1])
    lastPer.append(perDataAd[k - 1])
    lastTot.append(totG[k-1])
    lastTot.append(totT[k - 1])
    lastTot.append(totAc[k - 1])
    lastTot.append(totAd[k - 1])
    lastTotAll.append(allData[k-1])
    avgData.append(avgDataG)
    avgData.append(avgDataT)
    avgData.append(avgDataAc)
    avgData.append(avgDataAd)
    totData.append(totG)
    totData.append(totT)
    totData.append(totAc)
    totData.append(totAd)
    perData.append(perDataG)
    perData.append(perDataT)
    perData.append(perDataAc)
    perData.append(perDataAd)

    #Uncomment any of the print function below to print desired graph
    #printAvgGraph()
    #printTotGraph()
    #printPerGraph()
    #printTotGraphAll()
    #printAvgGraphP()
    #printPerGraphP()
    #printTotGraphP()
    #printTotAllGraphP()









