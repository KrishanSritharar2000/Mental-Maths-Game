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

def level1():
    level1Dict = {1:[0, "name","time"], 2:[0, "", ""], 3:[0, "", ""], 4:[0, "", ""], 5:[0, "", ""], 6:[0, "", ""], 7:[0, "", ""], \
                  8:[0, "", ""], 9:[0, "", ""], 10:[0, "", ""], 11:[0, "", ""], 12:[0, "", ""]}
    exportDict = open("level1.pickle", "wb")
    pickle.dump(level1Dict, exportDict)
    exportDict.close()

def loadLevel1():
    exportDict = open("level1.pickle", "rb")
    dict = pickle.load(exportDict)
    print(dict)
    print(dict[1][0])
    print(dict[1][1])
    print(dict[1][2])

def loadHighscore(level):
    fileNameList = ["l","e","v","e","l","-","p","i","c","k","l","e"]
    fileNameList.insert(5, str(level))
    fileName = "".join(fileNameList)
    print(fileName)
loadHighscore(2)
loadHighscore(1)

# level1()
# loadLevel1()
# statistics()
