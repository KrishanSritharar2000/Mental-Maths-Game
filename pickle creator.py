import pickle

def highscore():

    highscoreDict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    exportDict = open("highscore.pickle", "wb")
    pickle.dump(highscoreDict, exportDict)
    exportDict.close()

def statistics():
    statsDict = {"gamesPlayed":0, "questAnswered":0, "correctAnswerQuesEasy":0, "correctAnswerQuesMed":0, \
                 "correctAnswerQuesHard":0, "vehicleUnlock":0, "coinTotal":0, "coinSpent":0, "totalScore":0}
    exportDict = open("stats.pickle", "wb")
    pickle.dump(statsDict, exportDict)
    exportDict.close()

def statisticsRead():

    exportDict = open("stats.pickle", "rb")
    dict = pickle.load(exportDict)
    exportDict.close()
    print(dict)
    print(dict["vehicleUnlock"])



def createScoreDict(level):
    # levelDict = {0:[100, "name100","date100"], 1:[90, "test90", "date90"], 2:[80, "name80", "date80"], 3:[70, "test70", "date70"], \
    #               4:[60, "name60", "date60"], 5:[50, "test50", "date50"], 6:[40, "name40", "date40"],   7:[30, "test30", "date30"], \
    #               8:[20, "name20", "date20"], 9:[10, "test10", "date10"]}
    levelDict = {0:[0, "",""], 1:[0, "",""], 2:[0, "",""], 3:[0, "",""], 4:[0, "",""], 5:[0, "",""], \
                 6:[0, "",""], 7:[0, "",""], 8:[0, "",""], 9:[0, "",""]}
    fileNameList = ["l","e","v","e","l",".","p","i","c","k","l","e"]
    fileNameList.insert(5, str(level))
    pickleFile = "".join(fileNameList)
    exportDict = open(pickleFile, "wb")
    pickle.dump(levelDict, exportDict)
    exportDict.close()


def loadLevel(level):
    fileNameList = ["l","e","v","e","l",".","p","i","c","k","l","e"]
    fileNameList.insert(5, str(level))
    pickleFile = "".join(fileNameList)
    exportDict = open(pickleFile, "rb")
    dict = pickle.load(exportDict)
    print(dict)
    # print(dict[1][0])
    # print(dict[1][1])
    # print(dict[1][2])
    print(dict[2])
    # dict[5][0] = dict[6][0]
    dict[2][1] = "Ayub"
    # dict[5][2] = dict[6][2]
    # dict[6][0] = 0
    # dict[6][1] = ""
    # dict[6][2] = ""

    # exportDict = open(pickleFile, "wb")
    # pickle.dump(dict, exportDict)
    # exportDict.close()

def loadHighscore(level):
    fileNameList = ["l","e","v","e","l",".","p","i","c","k","l","e"]
    fileNameList.insert(5, str(level))
    fileName = "".join(fileNameList)
    print(fileName)
# loadHighscore(2)
# loadHighscore(1)

# createScoreDict(1)
# loadLevel(1)
# createScoreDict(2)
# loadLevel(2)
# createScoreDict(3)
# loadLevel(3)
# createScoreDict(4)
# loadLevel(1)
# createScoreDict(5)
# loadLevel(5)
# createScoreDict(6)
# loadLevel(6)
# createScoreDict(7)
# loadLevel(7)
# createScoreDict(8)
# loadLevel(8)
# createScoreDict(0)
# loadLevel(0)

# statistics()
statisticsRead()
