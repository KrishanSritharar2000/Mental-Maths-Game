import pygame as pg
from settings import *
from sprites import *
from os import path
from PIL import Image
import pickle

class Map:
    def __init__(self, filename, trackfile, bitSize=4):
        self.data = []
        with open(filename, 'rt') as file:
            for line in file:
                self.data.append(line.strip())
        file.close()

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

        self.trackData = []
        self.wallData = []
        self.fillData = []
        self.questionData = []
        self.trackImage = Image.open(trackfile)
        self.trackWidth = self.trackImage.size[0]
        self.trackHeight = self.trackImage.size[1]

        for col in range(self.trackHeight):
            for row in range(self.trackWidth):
                pixelData = self.trackImage.getpixel((row, col))
                if bitSize == 1:
                    if pixelData == 1:
                        self.trackData.append((row, col))
                else:
                    if pixelData == 0:
                        self.trackData.append((row, col))
                if bitSize == 4:
                    if pixelData == 5:
                        self.wallData.append((row, col))
                    if pixelData == 12:
                        self.fillData.append((row, col))
                    if pixelData == 2:
                        self.questionData.append((row, col))

        # print(self.trackData)
        # print()
        # print(self.wallData)
        # print()
        # print(self.fillData)
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def applyOffset(self, item):
        return item.rect.move(self.camera.topleft)

    def applyOffsetRect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        #limit scrolling to map size
        x = min(0, x) #left
        y = min(0, y) #top
        x = max(-(self.width - WIDTH), x) #right
        y = max(-(self.height - HEIGHT), y) #bottom

        self.camera = pg.Rect(x, y, self.width, self.height)

class sceneManager():
    def __init__(self, game):
        self.game = game
        self.currentScene = 'startScreen'
        self.backgroundColour = BLACK
        self.first = True
        self.prevScence = None
        self.secondPrevScence = None

    def loadLevel(self, level=None):
        self.level = level
        if self.level == "settingsMenu":
            self.settingsMenu()
        if self.level == "mainMenu":
            self.mainMenu()
        if self.level == "levelSelect":
            self.levelSelect()
        if self.level == "stats":
            self.stats()
        if self.level == "leaderboard":
            self.leaderboard()
        if self.level == "shop":
            self.shop()
        if self.level == "startScreen":
            self.startScreen()
        if self.level == "gameOverScreen":
            self.gameOverScreen()
        if self.level == "level1":
            self.level1()
        if self.level == "level2":
            self.level2()
        if self.level == "level3":
            self.level3()
        if self.level == "level4":
            self.level4()
        if self.level == "levelComplete":
            self.levelComplete()
        if self.level == "pause":
            self.pause()

    def level1(self):
        self.showPlayer = True
        self.game.map = Map(path.join(self.game.mapFolder,'map2.txt'), path.join(self.game.mapFolder,'Track3.bmp'), bitSize=1)
        self.game.camera = Camera(self.game.map.width, self.game.map.height)
        self.loadHighscore(1)
        for row, tiles in enumerate(self.game.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Platform(self.game, col, row, TILESIZE, TILESIZE, GREEN)

                # if tile == "2":
                #     Track(self.game, col, row, 2, 20, BLUE)

                if tile == "3":
                    Wall(self.game, col, row, RED)

                if tile == "4":
                    Wall(self.game, col, row, GREEN, altColour=ORANGE, mode="end")

                if tile == "P":
                    self.game.player = Player(self.game, col, row)

        for coordinates in range(len(self.game.map.trackData)):
            platformx = self.game.map.trackData[coordinates][0]
            platformy = self.game.map.trackData[coordinates][1]
            Platform(self.game, platformx, platformy, 1, 1, LIGHT_BLUE, 'track')

        Question(self.game, WIDTH/2, HEIGHT/2)
        Question(self.game, WIDTH*3/2, HEIGHT/2)
        Question(self.game, WIDTH*5/2, HEIGHT/2)

        Coin(self.game, WIDTH/4, HEIGHT/2)
        Coin(self.game, WIDTH*3/4, HEIGHT/2)
        Coin(self.game, WIDTH*5/4, HEIGHT/2)
        Coin(self.game, WIDTH*7/4, HEIGHT/2)
        Coin(self.game, WIDTH*9/4, HEIGHT/2)


        # self.pauseButton = Button(self.game, "pause", WIDTH*8/9, HEIGHT*1/12, 30, 30, YELLOW, LIGHT_BLUE, "", 18,self.game.pauseIMGWhite, self.game.pauseIMGBlack)

    # def oldCode():
        # for row, tiles in enumerate(self.game.mapTrack.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "2":
        #             Track(self.game, col, row, 2, TILESIZE_TRACK, BLUE)
        #
        #
        # for row, tiles in enumerate(self.game.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Platform(self.game, col*TILESIZE, row*TILESIZE, self.game.map.width, self.game.map.height, GREEN)
        #         if tile == "2":
        #             Platform(self.game, col*TILESIZE, row*TILESIZE, self.game.map.width, self.game.map.height, BLUE)
        #         if tile == "3":
        #             Wall(self.game, col*TILESIZE, row*TILESIZE, self.game.map.width, self.game.map.height, RED)
        #         if tile == "P":
        #             self.game.player = Player(self.game, col*TILESIZE, row*TILESIZE)
        #
        # self.game.map.tilewidth
        # self.game.map.tileheight
        #
        # Platform(self.game, 0, HEIGHT*7/8, WIDTH, HEIGHT/8, BLUE)
        # Platform(self.game, WIDTH, HEIGHT*7/8, WIDTH, HEIGHT/8, GREEN)
        # Platform(self.game, 2*WIDTH, HEIGHT*7/8, WIDTH, HEIGHT/8, BLUE)
        # pauseIMG = pg.transform.scale(self.game.pauseIMG, (30,30))
        # pauseIMGRect = pauseIMG.get_rect()
        # pauseIMGRect.center = (WIDTH*8/9, HEIGHT/12)
        # self.game.screen.blit(pauseIMG, pauseIMGRect)

    def level2(self):
        self.showPlayer = True
        self.game.map = Map(path.join(self.game.mapFolder,'map3.txt'), path.join(self.game.mapFolder,'Track4.bmp'), bitSize=1)
        self.game.camera = Camera(self.game.map.width, self.game.map.height)
        #
        for row, tiles in enumerate(self.game.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Platform(self.game, col, row, TILESIZE, TILESIZE, GREEN)
                if tile == "3":
                    Wall(self.game, col, row, RED)
                if tile == "P":
                    self.game.player = Player(self.game, col, row)

        for coordinates in range(len(self.game.map.trackData)):
            platformx = self.game.map.trackData[coordinates][0]
            platformy = self.game.map.trackData[coordinates][1]
            Platform(self.game, platformx, platformy, 1, 1, LIGHT_BLUE, 'track')

        self.pauseButton = Button(self.game, "pause", WIDTH*8/9, HEIGHT*1/12, 30, 30, YELLOW, LIGHT_BLUE, "", 18,self.game.pauseIMGWhite, self.game.pauseIMGBlack)

    def level3(self):
        self.showPlayer = True
        self.game.map = Map(path.join(self.game.mapFolder,'map2.txt'), path.join(self.game.mapFolder,'Track6.bmp'))
        self.game.camera = Camera(self.game.map.width, self.game.map.height)

        for row, tiles in enumerate(self.game.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Platform(self.game, col, row, 50, 50, GREEN)
                if tile == "3":
                    Wall(self.game, col, row, RED)
                if tile == "P":
                    self.game.player = Player(self.game, col, row)

        for coordinates in range(len(self.game.map.trackData)):
            trackx = self.game.map.trackData[coordinates][0]
            tracky = self.game.map.trackData[coordinates][1]
            Platform(self.game, trackx, tracky, 1, 1, LIGHT_BLUE, 'track')

        for coordinates in range(len(self.game.map.wallData)):
            wallx = self.game.map.wallData[coordinates][0]
            wally = self.game.map.wallData[coordinates][1]
            WallFile(self.game, wallx, wally, 1, 1, LIGHT_RED)

        for coordinates in range(len(self.game.map.fillData)):
            fillx = self.game.map.fillData[coordinates][0]
            filly = self.game.map.fillData[coordinates][1]
            Rectangle(self.game, fillx, filly, 1, 1, YELLOW)
            # pg.draw.rect(self.game.screen, YELLOW, [fillx, filly, 1, 1])

            # print(fillx, filly)
        self.pauseButton = Button(self.game, "pause", WIDTH*8/9, HEIGHT*1/12, 30, 30, YELLOW, LIGHT_BLUE, "", 18,self.game.pauseIMGWhite, self.game.pauseIMGBlack)

    def level4(self):
        self.showPlayer = True
        print("level4")
        self.game.map = Map(path.join(self.game.mapFolder,'map2.txt'), path.join(self.game.mapFolder,'Track7.bmp'))
        self.game.camera = Camera(self.game.map.width, self.game.map.height)

        for row, tiles in enumerate(self.game.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Platform(self.game, col, row, 50, 50, GREEN)
                if tile == "3":
                    Wall(self.game, col, row, RED)
                if tile == "P":
                    self.game.player = Player(self.game, col, row)

        for coordinates in range(len(self.game.map.trackData)):
            trackx = self.game.map.trackData[coordinates][0]
            tracky = self.game.map.trackData[coordinates][1]
            Platform(self.game, trackx, tracky, 1, 1, LIGHT_BLUE, 'track')

        for coordinates in range(len(self.game.map.wallData)):
            wallx = self.game.map.wallData[coordinates][0]
            wally = self.game.map.wallData[coordinates][1]
            WallFile(self.game, wallx, wally, 1, 1, LIGHT_RED)

        for coordinates in range(len(self.game.map.fillData)):
            fillx = self.game.map.fillData[coordinates][0]
            filly = self.game.map.fillData[coordinates][1]
            Rectangle(self.game, fillx, filly, 1, 1, YELLOW)

        for coordinates in range(len(self.game.map.questionData)):
            fillx = self.game.map.questionData[coordinates][0]
            filly = self.game.map.questionData[coordinates][1]
            Question(self.game, fillx, filly)

    def levelComplete(self):
        self.image = pg.transform.scale(self.game.menuImages[self.currentScene], (WIDTH, HEIGHT))
        rect = self.image.get_rect()
        self.game.screen.blit(self.image, rect)
        self.game.drawText("Level Completed", 30, WHITE, WIDTH/2, HEIGHT/6, fontName=self.game.interfaceFont)
        nextLevelTagNumber = int(self.prevScence[-1]) + 1
        levelList = list(self.prevScence)
        levelList[-1] = str(nextLevelTagNumber)
        nextLevel = "".join(levelList)
        print("Next Level: ", nextLevel)
        if self.game.score > self.highscore:
            self.updateHighscore(nextLevelTagNumber-1, self.game.score)
            self.game.drawText("Congratulations, new High Score", 28, WHITE, WIDTH/2, HEIGHT*5/11, fontName=self.game.interfaceFont)
        self.game.drawText("Score: {}".format(str(self.game.score)), 25, WHITE, WIDTH/2, HEIGHT*3/11, fontName=self.game.buttonFont)
        self.game.drawText("Highscore: {}".format(str(self.highscore)), 25, WHITE, WIDTH/2, HEIGHT*4/11, fontName=self.game.interfaceFont)

        self.game.drawText("Coins Collected: {}".format(self.coinCollected), 25, WHITE, WIDTH/2, HEIGHT*5/11, fontName=None)
        self.game.drawText("Total Coins: {}".format(self.game.coinAmount), 25, WHITE, WIDTH/2, HEIGHT*6/11, fontName=None)

        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/4, HEIGHT*6/8, WIDTH/5, HEIGHT/6, YELLOW, LIGHT_BLUE, "Main Menu")
        self.nextLevel = Button(self.game, nextLevel, WIDTH /2, HEIGHT*6/8, WIDTH/5, HEIGHT/6, YELLOW, LIGHT_BLUE, "Next Level")
        self.levelSelectButton = Button(self.game, "levelSelect", WIDTH*3/4, HEIGHT*6/8, WIDTH/5, HEIGHT/6, YELLOW, LIGHT_BLUE, "Select Level")

    def oldloadHighscore(self, level):
        highscoreFile = open("highscore.pickle", "rb")
        self.highscoreDict = pickle.load(highscoreFile)
        highscoreFile.close()
        self.highscore = self.highscoreDict[level]
        print("highscoreDict: ", self.highscoreDict)
        print("highscore", self.highscore)

    def loadHighscore(self, level):
        fileNameList = ["l","e","v","e","l",".","p","i","c","k","l","e"]
        fileNameList.insert(5, str(level))
        self.levelFileName = "".join(fileNameList)
        highscoreFile = open(self.levelFileName, "rb")
        self.highscoreDict = pickle.load(highscoreFile)
        highscoreFile.close()
        self.highscore = self.highscoreDict[0]#the scores will be in order
        print("highscoreDict: ", self.highscoreDict)
        print("highscore", self.highscore)


    def updateHighscore(self, level, score):
        self.oldHighscore = self.highscoreDict[level]
        self.practiceDict = self.highscoreDict
        self.scoreName = "test"
        self.scoreDate = "1/1/1"
        placed = False
        self.index = 11
        for i in range(10):
            if score > self.practiceDict[9-i][0]:
                self.index = 9-i
        print(practiceDict)
        print(index)
        addedScore = True
        for i in range(10-self.index):
            tempScore = self.practiceDict[index+i][0]
            tempName = self.practiceDict[index+i][1]
            tempDate = self.practiceDict[index+i][2]
            if addedScore:
                self.practiceDict[index+i][0] = score
                self.practiceDict[index+i][1] = self.scoreName
                self.practiceDict[index+i][2] = self.scoreDate
                addedScore = False
            else:
                self.practiceDict[index+i][0] = tempScore
                self.practiceDict[index+i][1] = tempName
                self.practiceDict[index+i][2] = tempDate

        # self.highscoreDict[level] = score
        self.highscore = score
        highscoreWriteFile = open(self.levelFileName,"wb")
        pickle.dump(self.highscoreDict, highscoreWriteFile)
        highscoreWriteFile.close()

        print("highscoreDict before writing", self.highscoreDict)
        print("score", score)
        print("highscoreDict after writing", self.highscoreDict)


    def pause(self):
        # self.game.drawText("Pause Menu", 25, WHITE, WIDTH/2, HEIGHT*1/9, surf= self.game.pauseScreen, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*3/8, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Main Menu")
        self.resumeButton = Button(self.game, "resume", WIDTH*5/8, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Resume")
        # self.game.paused = True

    def settingsMenu(self):
        self.game.drawText("Settings", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/9, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.startScreenButton = Button(self.game, "startScreen", WIDTH/4, HEIGHT*3/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "View Start Screen")

    def levelSelect(self):
        self.game.drawText("Select Level", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.level1Button = Button(self.game, "level1", WIDTH*1/2, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level One")
        self.level2Button = Button(self.game, "level2", WIDTH*1/2, HEIGHT*5/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level Two")
        self.level3Button = Button(self.game, "level3", WIDTH*1/2, HEIGHT*3/4, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level Three")
        self.level4Button = Button(self.game, "level4", WIDTH*1/2, HEIGHT*7/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level Four")

    def stats2(self):
        self.game.drawText("View your statistics", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        correctAnswerQuest = self.game.correctAnswerQuesEasy + self.game.correctAnswerQuesMed + self.game.correctAnswerQuesHard
        incorrectAnswerQuest = self.game.questAnswered - correctAnswerQuest
        averageScore = int(round(self.game.totalScore / self.game.gamesPlayed,0))
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.game.drawText("Number of Questions Answered: {}".format(self.game.questAnswered), 18, WHITE, WIDTH/2, HEIGHT*3/11)
        self.game.drawText("Correctly Answered Questions: {}".format(correctAnswerQuest), 18, WHITE, WIDTH/2, HEIGHT*4/11)
        self.game.drawText("Incorrectly Answered Questions: {}".format(incorrectAnswerQuest), 18, WHITE, WIDTH/2, HEIGHT*5/11)
        self.game.drawText("Question for each Difficulty: {}".format("0"), 18, WHITE, WIDTH/2, HEIGHT*6/11)
        self.game.drawText("Total Vehicles Unlocked: {}".format("0"), 18, WHITE, WIDTH/2, HEIGHT*7/11)
        self.game.drawText("Total Games Played: {}".format(self.game.gamesPlayed), 18, WHITE, WIDTH/2, HEIGHT*8/11)
        self.game.drawText("Total Coins Collected: {}".format(self.game.coinAmount), 18, WHITE, WIDTH/2, HEIGHT*9/11)
        self.game.drawText("Total Score / Average Score: {} / {}".format(self.game.totalScore, averageScore), 18, WHITE, WIDTH/2, HEIGHT*10/11)

    def stats(self):
        self.game.drawText("View your statistics", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        correctAnswerQuest = self.game.correctAnswerQuesEasy + self.game.correctAnswerQuesMed + self.game.correctAnswerQuesHard
        incorrectAnswerQuest = self.game.questAnswered - correctAnswerQuest
        averageScore = int(round(self.game.totalScore / self.game.gamesPlayed,0))
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.game.drawText("Number of Questions Answered:", 18, WHITE, WIDTH*3/8, HEIGHT*3/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format(self.game.questAnswered), 18, WHITE, WIDTH*3/4, HEIGHT*3/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Correctly Answered Questions:", 18, WHITE, WIDTH*3/8, HEIGHT*4/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format(correctAnswerQuest), 18, WHITE, WIDTH*3/4, HEIGHT*4/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Incorrectly Answered Questions:", 18, WHITE, WIDTH*3/8, HEIGHT*5/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format(incorrectAnswerQuest), 18, WHITE, WIDTH*3/4, HEIGHT*5/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Question for each Difficulty:", 18, WHITE, WIDTH*5/16, HEIGHT*6/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Easy: {}     Medium: {}     Hard: {}".format(self.game.correctAnswerQuesEasy, self.game.correctAnswerQuesMed,\
                                    self.game.correctAnswerQuesHard), 18, WHITE, WIDTH*3/4, HEIGHT*6/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Total Vehicles Unlocked:", 18, WHITE, WIDTH*3/8, HEIGHT*7/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format("0"), 18, WHITE, WIDTH*3/4, HEIGHT*7/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Total Games Played:", 18, WHITE, WIDTH*3/8, HEIGHT*8/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format(self.game.gamesPlayed), 18, WHITE, WIDTH*3/4, HEIGHT*8/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Total Coins Collected:", 18, WHITE, WIDTH*3/8, HEIGHT*9/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{}".format(self.game.coinAmount), 18, WHITE, WIDTH*3/4, HEIGHT*9/11, fontName=self.game.interfaceFont2)
        self.game.drawText("Total Score / Average Score:", 18, WHITE, WIDTH*3/8, HEIGHT*10/11, fontName=self.game.interfaceFont2)
        self.game.drawText("{} / {}".format(self.game.totalScore, averageScore), 18, WHITE, WIDTH*3/4, HEIGHT*10/11, fontName=self.game.interfaceFont2)

    def leaderboard(self):
        self.game.drawText("Leader Board Tables", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)


    def shop(self):
        self.game.drawText("Spend your coins in the shop", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

    def mainMenu(self):
        if self.image != pg.transform.scale(self.game.menuImages["mainMenu"], (WIDTH, HEIGHT)):
            image = pg.transform.scale(self.game.menuImages["mainMenu"], (WIDTH, HEIGHT))
            rect = image.get_rect()
            self.game.screen.blit(image, rect)
        self.game.drawText("Main Menu", 30, WHITE, WIDTH/2, HEIGHT*1/8, fontName=self.game.interfaceFont)
        self.levelSelectButton = Button(self.game, "levelSelect", WIDTH*1/2, HEIGHT*3/8, WIDTH/3, HEIGHT/6, YELLOW, LIGHT_BLUE, "Select Level")
        self.settingsMenuButton = Button(self.game, "settingsMenu", WIDTH/4, HEIGHT*5/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Settings")
        self.shopButton = Button(self.game, "shop", WIDTH*3/4, HEIGHT*5/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Shop")
        self.leaderboardButton = Button(self.game, "stats", WIDTH/4, HEIGHT*7/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Stats")
        self.statsButton = Button(self.game, "leaderboard", WIDTH*3/4, HEIGHT*7/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Leaderboard")

    def startScreen(self):
        #game spalsh/start screen
        self.image = pg.transform.scale(self.game.menuImages["startScreen"], (WIDTH, HEIGHT))
        rect = self.image.get_rect()
        self.game.screen.blit(self.image, rect)
        self.game.drawText("Game Title", 32, WHITE, WIDTH/2, HEIGHT*1/4)
        self.game.drawText("Press A Button To Continue!", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.waitForKey()
        self.loadLevel('mainMenu')

    def gameOverScreen(self):
        #game over/continue screen
        pass

    def waitForKey(self, key = True, click = True):#key contiues if a key is get_pressed
        pg.event.wait()#click continues if the mouse button is pressed
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    # waiting = self.game.running = False
                if event.type == pg.KEYUP and key:
                    waiting = False
                if event.type == pg.MOUSEBUTTONUP and click:
                    waiting = False

    def waitForButtonPress(self, button, clicked):
        while clicked == False:
            button.update()
            pg.display.flip()

    def update(self):
        # pg.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.buttons.update()
        # pg.display.flip()
        for button in self.game.buttons:

            if button.clicked == True:
                # print("tag",button.tag)
                if button.tag not in ("2", "3", "4", "5", "6"):
                    self.secondPrevScence = self.prevScence
                    self.prevScence = self.currentScene
                    self.currentScene = button.tag

                    print("2nd Prev: {}, Prev: {}, Current: {} ButtonTag: {}".format(self.secondPrevScence, self.prevScence, self.currentScene, button.tag))
                    if button.tag not in ('level1', 'level2', 'level3','level4', 'pause', 'resume', 'levelComplete'):
                        self.image = pg.transform.scale(self.game.menuImages[self.currentScene], (WIDTH, HEIGHT))
                        rect = self.image.get_rect()
                        self.game.screen.blit(self.image, rect)
                    elif button.tag in ('level1', 'level2', 'level3', "level4"):#creation of a new level
                        for wall in self.game.walls:
                            wall.kill()
                        for endWall in self.game.endWalls:
                            endWall.kill()
                        for platform in self.game.platforms:
                            platform.kill()
                        for rectangle in self.game.rectangles:
                            rectangle.kill()
                        for questions in self.game.questionItems:
                            questions.kill()
                        if self.game.player != None:
                            self.game.player.kill()

                        self.loadHighscore(int(self.currentScene[-1]))

                        self.game.score = 0
                        self.coinCollected = 0
                        self.game.gamesPlayed += 1

                    if button.tag == "startScreen":
                        self.loadLevel('startScreen')
                    if button.tag == "levelSelect":
                        self.loadLevel('levelSelect')
                    if button.tag == "shop":
                        self.loadLevel('shop')
                    if button.tag == 'mainMenu':
                        if self.game.paused:
                            self.game.paused = False
                        self.loadLevel('mainMenu')
                    if button.tag == "settingsMenu":
                        self.loadLevel('settingsMenu')
                    if button.tag == 'leaderboard':
                        self.loadLevel('leaderboard')
                    if button.tag == 'stats':
                        self.loadLevel('stats')
                    if button.tag == 'level1':
                        self.loadLevel('level1')
                    if button.tag == 'level2':
                        self.loadLevel('level2')
                    if button.tag == 'level3':
                        self.loadLevel('level3')
                    if button.tag == 'level4':
                        self.loadLevel('level4')
                    if button.tag == "levelComplete":
                        self.loadLevel('levelComplete')
                    if button.tag == 'pause':
                        self.loadLevel('pause')
                    if button.tag == 'resume':
                        self.game.paused = False
                        for button in self.game.buttons:
                            button.kill()
                        self.game.pauseScreenPrinted = False
                        self.currentScene = self.prevScence
                else:
                    self.game.answerClicked = True
                    self.game.selectedAns = self.game.questionData[self.game.questionNumberIndex][int(button.tag)]
                    if button.tag == "2":
                        self.game.answerCorrect = True
                    else:
                        self.game.answerCorrect = False
                    for button in self.game.buttons:
                        button.kill()

                    # self.game.pauseScreen.blit(self.game.pauseScreenImage, self.game.pauseScreenImageRect)
                    # self.game.pauseScreen.fill((123, 129, 140))
                #     self.loadLevel('pause')
                button.kill()
        if self.currentScene  not in ("level1", "level2", "level3", "level4"):
            self.showPlayer = False
            # print("showPlayer :", self.showPlayer)
        else:
            self.showPlayer = True
