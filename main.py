import pygame as pg
from os import path
import random
import csv
from settings import *
from sprites import *
from management import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        #initializes game window
        pg.init()
        pg.mixer.init()#This handles all the sound and music in the game
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#This creates the screen with the specified dimensions
        pg.display.set_caption(TITLE)#sets the title of the window
        self.clock = pg.time.Clock()#starts the internal clock to sync the program
        self.running = True
        self.loadData()

    def loadData(self):
        self.gameFolder = path.dirname(__file__)
        self.imgFolder = path.join(self.gameFolder, 'img')
        self.mapFolder = path.join(self.gameFolder, 'map')
        self.interfaceFont = path.join(self.imgFolder, 'Future.ttf')
        self.interfaceFont2 = path.join(self.imgFolder, 'FutureNarrow.ttf')
        self.buttonFont = path.join(self.imgFolder, 'PixelSquare.ttf')
        self.menuButtonSolid = pg.image.load(path.join(self.imgFolder, 'blue_button01.png')).convert_alpha()
        self.menuButtonHighlight = pg.image.load(path.join(self.imgFolder, 'green_button01.png')).convert_alpha()

        self.menuImages = {}
        self.menuImages["startScreen"] =  pg.image.load(path.join(self.imgFolder, 'grey_background.jpg')).convert_alpha()
        self.menuImages["mainMenu"] =  pg.image.load(path.join(self.imgFolder, 'blue_background.jpg')).convert_alpha()
        self.menuImages["settingsMenu"] =  pg.image.load(path.join(self.imgFolder, 'Grey_yellow_background.jpg')).convert_alpha()
        self.menuImages["levelSelect"] =  pg.image.load(path.join(self.imgFolder, 'Grey_blue_background.jpg')).convert_alpha()
        self.menuImages["stats"] =  pg.image.load(path.join(self.imgFolder, 'Grey_green_background.jpg')).convert_alpha()
        self.menuImages["leaderboard"] =      pg.image.load(path.join(self.imgFolder, 'Grey_violet_background.jpg')).convert_alpha()
        self.menuImages["shop"] =  pg.image.load(path.join(self.imgFolder, 'Grey_orange_background.jpg')).convert_alpha()
        self.menuImages["pause"] =  pg.image.load(path.join(self.imgFolder, 'Grey_red_background.jpg')).convert_alpha()
        self.menuImages["levelComplete"] =  pg.image.load(path.join(self.imgFolder, 'blue_background.jpg')).convert_alpha()

        self.pauseScreen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.pauseScreenImage = pg.transform.scale(self.menuImages['pause'], (WIDTH, HEIGHT))
        self.pauseScreenImageRect = self.pauseScreenImage.get_rect()
        self.pauseScreen.blit(self.pauseScreenImage, self.pauseScreenImageRect)
        self.drawText("Pause Menu", 25, WHITE, WIDTH/2, HEIGHT*1/9, surf=self.pauseScreen, fontName=self.interfaceFont)    #wasnt being printed before because it was before the previous line
        self.pauseIMGWhite = pg.image.load(path.join(self.imgFolder, 'pauseWhite.png')).convert_alpha()
        self.pauseIMGBlack = pg.image.load(path.join(self.imgFolder, 'pauseBlack.png')).convert_alpha()

        self.carImage = pg.image.load(path.join(self.imgFolder, 'car.png')).convert_alpha()
        self.carImgSize = self.carImage.get_size()
        self.carImage = pg.transform.scale(self.carImage, (int(round(self.carImgSize[0]/6,0)), int(round(self.carImgSize[1]/6,0))))

        self.bikeImage = pg.image.load(path.join(self.imgFolder, 'bike.png')).convert_alpha()
        self.bikeImgSize = self.bikeImage.get_size()
        self.bikeImage = pg.transform.scale(self.bikeImage, (int(round(self.bikeImgSize[0]/10,0)), int(round(self.bikeImgSize[1]/10,0))))
        self.playerImage = self.carImage

        if self.playerImage == self.carImage:
            self.imageType = "car"
        elif self.playerImage == self.bikeImage:
            self.imageType = "bike"

        self.loadQuestions()
        self.questionSurface = pg.Surface(self.screen.get_size()).convert_alpha()

        self.loadstatsData()

        self.coinImages = {}
        for img in range(len(COIN_IMAGES)):
            image = pg.image.load(path.join(self.imgFolder, COIN_IMAGES[img])).convert_alpha()
            size = image.get_size()
            self.coinImages[img] = pg.transform.scale(image, (int(size[0]/2), int(size[1]/2)))

        self.questionImage = pg.image.load(path.join(self.imgFolder, QUESTION_IMAGE)).convert_alpha()

    def loadstatsData(self):
        statsFile = open("stats.pickle", "rb")
        self.statsData = pickle.load(statsFile)
        statsFile.close()
        self.coinAmount = self.statsData["coinTotal"]
        self.gamesPlayed = self.statsData["gamesPlayed"]
        self.questAnswered = self.statsData["questAnswered"]
        self.correctAnswerQuesEasy = self.statsData["correctAnswerQuesEasy"]
        self.correctAnswerQuesMed = self.statsData["correctAnswerQuesMed"]
        self.correctAnswerQuesHard = self.statsData["correctAnswerQuesHard"]
        self.vehicleUnlock = self.statsData["vehicleUnlock"]
        self.coinSpent = self.statsData["coinSpent"]
        self.totalScore = self.statsData["totalScore"]

        print("Loaded stats fle")
        print("statsDict: ", self.statsData)
        print("coinAmount", self.coinAmount)
        print("coinAmount 0")

    def updateStatsData(self):
        statsFile = open("stats.pickle", "wb")
        self.statsData["coinTotal"] = self.coinAmount
        self.statsData["gamesPlayed"] = self.gamesPlayed
        self.statsData["questAnswered"] = self.questAnswered
        self.statsData["correctAnswerQuesEasy"] = self.correctAnswerQuesEasy
        self.statsData["correctAnswerQuesMed"] = self.correctAnswerQuesMed
        self.statsData["correctAnswerQuesHard"] = self.correctAnswerQuesHard
        self.statsData["vehicleUnlock"] = self.vehicleUnlock
        self.statsData["coinSpent"] = self.coinSpent
        self.statsData["totalScore"] = self.totalScore
        pickle.dump(self.statsData, statsFile)
        statsFile.close()

    def loadQuestions(self):
        questionCSV = path.join(self.gameFolder, 'questions.csv')
        with open(questionCSV, 'r') as questionFile:
            reader = csv.reader(questionFile)
            next(questionFile)
            self.questionData = []
            self.questionID = []
            for line in reader:
                temp = []
                questionID = int(line[0])
                question = str(line[1])
                cAns = (line[2])
                wAns1, wAns2, wAns3, wAns4 = (line[3]),(line[4]),(line[5]),(line[6])
                diff = str(line[7])
                level = int(line[8])
                isMaj = str(line[9])
                self.questionID.append(questionID)
                temp.extend((questionID,question,cAns,wAns1,wAns2,wAns3,wAns4,diff,level,isMaj))
                self.questionData.append(temp)
        questionFile.close()
        print(self.questionData)

                # line = [QuestionID, Questtion, CAns, WAns1, Wans2, Wans3, Wans4, Diff, level, isMaj]

    def drawText(self, text, size, colour, x, y, surf=None, align=None, fontName=None):
        if surf == None:
            surf = self.screen
        fontType = "C:\WINDOWS\FONTS\ARIAL.TTF"
        if fontName == None:
            font = pg.font.SysFont('arial', size)
        else:
            font = pg.font.Font(fontName, size)
        textSurface = font.render(text, True, colour)
        textRect = textSurface.get_rect()
        if align == None:
            textRect.center = (int(x),int(y))#aligns the text to the center
        if align == "tl":
            textRect.topleft = (int(x),int(y))
        surf.blit(textSurface, textRect)

    def new(self):
        #start a new Game
        self.allSprites = pg.sprite.LayeredUpdates()#This groups all the sprites together
        self.buttons = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.rectangles = pg.sprite.Group()    #This is the area under the track
        self.questionItems = pg.sprite.Group()
        self.endWalls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.userInputBox = pg.sprite.Group()
        self.map = None
        self.tiledMap = None
        self.tiledMapImg = None
        self.tiledMapRect = None
        self.camera = None
        #Map(path.join(self.gameFolder,'map2.txt', 'LevelTest2'))
        #Camera(self.map.width, self.map.height)
        self.sceneMan = sceneManager(self)
        self.player = None
        self.paused = False
        self.pauseScreenPrinted = False
        self.askQuestion = False
        self.questionScreenPrinted = False
        # with open(path.join(self.gameFolder, 'highscore'), 'r') as highScore:
        #     try:
        #         self.highscore = int(f.read())
        #     except:
        #         self.highscore = 0
        self.score = 0
        self.delay = False
        self.lastCountdownTime = 0
        self.prevRotate = 0
        self.settingsQuestionDiff = "easy"
        self.questionID = []
        for i in range(len(self.questionData)):
            if self.questionData[i][7] == self.settingsQuestionDiff:
                if self.questionData[i][9] == 'FALSE':
                    self.questionID.append(self.questionData[i][0])
                    print("This is the Question:", self.questionData[i][1], self.questionData[i][9])
        self.majorQuestion = False
        self.majorQuestionCorrect = True
        self.sceneMan.loadLevel('startScreen')
        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #get the time of the previous frame in seconds
            self.events()
            self.update()
            self.draw()

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        #Game loop - Update
        self.sceneMan.update()
        # print("Paused variable state: ", self.paused)
        if not self.paused:
            # print("Doing Update function")
            self.allSprites.update()#Updates all of the sprties at once
            self.userInputBox.update()
            if self.sceneMan.currentScene not in MENU_SCREENS:
                self.camera.update(self.player)

                hitPlatform = pg.sprite.spritecollide(self.player, self.platforms, False)
                if hitPlatform:
                    # if hitPlatform[0].mode == "track":
                    #     if self.player.vel.x > 0:
                    #         self.player.pos.y = hitPlatform[-1].rect.topright[1ddd] - self.player.height / 2
                    #     else:
                    #         self.player.pos.y = hitPlatform[-1].rect.topleft[1] - self.player.height / 2
                    #     self.player.vel.y = 0
                    #
                    # else:
                    self.player.pos.y = hitPlatform[0].rect.y - self.player.height / 2
                    self.player.vel.y = 0

                    self.vecToPlayer = self.player.pos - vec(0, HEIGHT)
                    # if hitPlatform[0].mode == "track":
                    #     # print("DOING")
                    #     # print("velx, vely", self.player.vel.x, self.player.vel.y)
                    #     if self.player.vel.x > 0 and self.player.vel.y > 0:
                    #         self.player.image = pg.transform.rotate(self.playerImage, 45)
                    #     elif self.player.vel.x > 0 and self.player.vel.y > 0:
                    #         self.player.image = pg.transform.rotate(self.playerImage, 315)
                    # else:
                    #     self.player.image = self.playerImage
                    # self.rotate = self.vecToPlayer.angle_to(vec(1, 0))
                    # print(self.player.pos)
                    # print(self.rotate)
                    # if self.prevRotate != round(self.rotate,2):
                    #     self.player.image = self.rot_center(self.player.image, self.rotate)
                    #     # self.player.image = pg.transform.rotate(self.player.image, self.rotate)
                    #     # self.player.rect = self.player.image.get_rect()
                    #     # self.player.rect.center = self.player.pos
                    #     self.prevRotate = round(self.rotate,2)

                hitQuestion = pg.sprite.spritecollide(self.player, self.questionItems, False)
                if hitQuestion:
                    pg.display.update()
                    hitQuestion = pg.sprite.spritecollide(self.player, self.questionItems, True, pg.sprite.collide_mask)
                    if hitQuestion:
                        self.askQuestion = True
                        self.paused = True
                        if hitQuestion[0].major == True:
                            self.majorQuestion = True

                hitCoin =  pg.sprite.spritecollide(self.player, self.coins, True)
                if hitCoin:
                    print("A Coin has been hit")
                    self.coinAmount += 1
                    self.sceneMan.coinCollected += 1
                    print("Total Coins: {}".format(self.coinAmount))

                hitLevelEnd = pg.sprite.spritecollide(self.player, self.endWalls, True)
                if hitLevelEnd:
                    self.totalScore += self.score
                    print("Hit Wall")
                    print("Total Score", self.totalScore)
                    self.majorQuestion = False

                    self.sceneMan.secondPrevScence = self.sceneMan.prevScence
                    self.sceneMan.prevScence = self.sceneMan.currentScene
                    self.sceneMan.currentScene = "levelComplete"
                    self.sceneMan.showPlayer = False
                    self.sceneMan.loadLevel("levelComplete")


    def events(self):
        #Game loop - Events1
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                self.updateStatsData()
                if self.playing:
                    self.playing = False
                    self.running = False

            for box in self.userInputBox:
                box.inputKeys(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_p:
                    if self.sceneMan.currentScene in LEVEL_SCREENS:
                        self.paused = not self.paused
                        if self.paused == False:
                            for button in self.buttons:
                                button.kill()
                        self.pauseScreenPrinted = False
                if event.key == pg.K_q:
                    print("Q button pressed")
                    print("self.askQuestion is: ", self.askQuestion)
                    self.askQuestion = not self.askQuestion
                    if self.askQuestion:
                        self.paused = True
                    else:
                        self.paused = False
                        self.questionScreenPrinted = False

    def getQuestion(self):
        self.answerCorrect = False
        self.answerClicked = False
        self.selectedAns = None
        self.startTime = pg.time.get_ticks()
        print("this is the question data", self.questionData)

        if self.majorQuestion == True:
            self.questionID = []

            for i in range(len(self.questionData)):
                if self.questionData[i][9] == 'TRUE':
                    if self.questionData[i][7] == self.settingsQuestionDiff:
                        print("This is the Question:", self.questionData[i][1], self.questionData[i][9])
                        self.questionID.append(self.questionData[i][0])

        questionNumber = random.choice(self.questionID)
        wrongAns = [3,4,5,6]
        chosenAns = [2,]
        print(self.questionID)
        print(questionNumber)
        # self.questionID.remove(questionNumber)
        print(self.questionID)
        self.questionNumberIndex = questionNumber - 1
        correctAns = self.questionData[self.questionNumberIndex][2]
        print(correctAns)

        for i in range(3):
            randomIndex = random.choice(wrongAns)
            wrongAns.remove(randomIndex)
            chosenAns.append(randomIndex)
        random.shuffle(chosenAns)

        self.drawText(str(self.questionData[self.questionNumberIndex][1]), 30, HUD_COLOUR, WIDTH/2, HEIGHT*2/9, surf=self.questionSurface)
        print("text to be printed {}".format(str(self.questionData[self.questionNumberIndex][1])))

        answer1 = Button(self, str(chosenAns[0]), WIDTH/3, HEIGHT/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, str(self.questionData[self.questionNumberIndex][chosenAns[0]]))
        answer2 = Button(self, str(chosenAns[1]), WIDTH*2/3, HEIGHT/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, str(self.questionData[self.questionNumberIndex][chosenAns[1]]))
        answer3 = Button(self, str(chosenAns[2]), WIDTH/3, HEIGHT*2/3, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, str(self.questionData[self.questionNumberIndex][chosenAns[2]]))
        answer4 = Button(self, str(chosenAns[3]), WIDTH*2/3, HEIGHT*2/3, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, str(self.questionData[self.questionNumberIndex][chosenAns[3]]))

    def getTimeAllowed(self):
        if self.questionData[self.questionNumberIndex][7] == "easy":
            self.questionDiff = "easy"
            self.timeAllowed = TIME_FOR_EASY_Q
        if self.questionData[self.questionNumberIndex][7] == "medium":
            self.questionDiff = "medium"
            self.timeAllowed = TIME_FOR_MEDIUM_Q
        if self.questionData[self.questionNumberIndex][7] == "hard":
            self.questionDiff = "hard"
            self.timeAllowed = TIME_FOR_HARD_Q
        self.timeRemaining = self.timeAllowed
        self.timeOut = False

    def calculateScore(self):
        self.timeTaken = int(round((self.endTime - self.startTime) / 1000, 0))

        print("The time take to answer that question was: ", self.timeTaken)

        multiplier = random.choice([2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,8,8,8,8,9,9,10,15])

        scoreIncrease = int(round((self.timeAllowed - self.timeTaken) * multiplier, 0))
        self.score += scoreIncrease
        print(self.score)

    def countdownTimer(self):
        now = pg.time.get_ticks()
        if now - self.lastCountdownTime > 1000 and self.timeRemaining >= 0:
            self.questionSurface.fill(WHITE, (WIDTH*7/8-80, HEIGHT/8-25, 160, 50))
            self.lastCountdownTime = now
            print("Time Remaining: {}".format(self.timeRemaining))
            self.drawText("Time Remaining: {}".format(self.timeRemaining), 20, HUD_COLOUR, WIDTH*7/8, HEIGHT/8, surf=self.questionSurface)
            self.timeRemaining -= 1
        if self.timeRemaining == -1:
            self.timeOut = True
            self.answerClicked = True
            if self.majorQuestion:
                self.majorQuestionCorrect = False

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        if self.paused:
            if self.askQuestion:
                if self.questionScreenPrinted == False:
                    self.questionSurface.fill(0)
                    self.drawText("Question asking", 25, HUD_COLOUR, WIDTH/2, HEIGHT*1/9, surf=self.questionSurface, fontName=self.interfaceFont)
                    self.getQuestion()
                    self.getTimeAllowed()
                    print("The question: {} The correct answer: {}".format(self.questionData[self.questionNumberIndex][1], self.questionData[self.questionNumberIndex][2]))
                    self.questionScreenPrinted = True

                for button in self.buttons:
                    button.draw(self.questionSurface)

                if self.answerClicked:
                    self.questAnswered += 1
                    self.endTime = pg.time.get_ticks()

                    if self.answerCorrect:
                        if self.questionDiff == "easy":
                            self.correctAnswerQuesEasy += 1
                        elif self.questionDiff == "medium":
                            self.correctAnswerQuesMed += 1
                        elif self.questionDiff == "hard":
                            self.correctAnswerQuesHard += 1
                        print("CORRECT ANSWER CHOSEN: {}".format(self.selectedAns))
                        self.calculateScore()
                        self.drawText("Correct Answer", 35, GREEN, WIDTH/2, HEIGHT*5/6, surf=self.questionSurface)
                    elif self.timeOut:
                        self.drawText("Time Out", 25, RED, WIDTH/2, HEIGHT*5/6, surf=self.questionSurface)
                        self.drawText("Correct Answer was {}".format(self.questionData[self.questionNumberIndex][2]), 20, HUD_COLOUR, WIDTH/2, HEIGHT*5/6 + 50, surf=self.questionSurface)
                        print("Time out, INCORRECT ANSWER CHOSEN: {}".format(self.selectedAns))
                        for button in self.buttons:
                            button.kill()
                    else:
                        if self.majorQuestion:
                            self.majorQuestionCorrect = False
                        print("INCORRECT ANSWER CHOSEN: {}".format(self.selectedAns))
                        self.drawText("Incorrect Answer", 25, RED, WIDTH/2, HEIGHT*5/6, surf=self.questionSurface)
                        self.drawText("Correct Answer was {}".format(self.questionData[self.questionNumberIndex][2]), 20, HUD_COLOUR, WIDTH/2, HEIGHT*5/6 + 50, surf=self.questionSurface)

                    print("major quesion", self.majorQuestionCorrect)
                    self.screen.blit(self.questionSurface, self.questionSurface.get_rect())
                    pg.display.flip()
                    pg.time.delay(1500)

                    self.askQuestion = False
                    self.questionScreenPrinted = False
                    self.paused = False

                else:
                    self.countdownTimer()

                self.screen.blit(self.questionSurface, self.questionSurface.get_rect())

            else:
                if self.pauseScreenPrinted == False:
                    self.sceneMan.loadLevel('pause')
                    self.pauseScreenPrinted = True
                for button in self.buttons:
                    button.draw(self.pauseScreen)
                self.screen.blit(self.pauseScreen, self.pauseScreen.get_rect())

                #self.screen.blit(self.pauseScreenImage, self.pauseScreenImageRect)

        else:
            for button in self.buttons:
                button.draw(self.screen)
            for box in self.userInputBox:
                box.draw(self.screen)
            if self.sceneMan.currentScene not in MENU_SCREENS:
                self.screen.blit(self.tiledMapImg, self.camera.applyOffsetRect(self.tiledMapRect))
                for sprite in self.allSprites:
                    self.screen.blit(sprite.image, self.camera.applyOffset(sprite))
                self.drawText("Score: " + str(self.score), 22, HUD_COLOUR, WIDTH-100, 15)
                self.drawText("Coin: " + str(self.coinAmount), 22, HUD_COLOUR, 100, 15)
        pg.display.flip()
        # if self.delay:
        #     pg.time.delay(1500)
        #     self.delay = False
        #used for buffered frames- ALWAYS DO THIS LAST AFTER DRAWING EVERYTHING

        # print('paused', self.paused)
        # print("self.buttons", self.buttons, self.paused, self.sceneMan.currentScene )
        # print("2nd Prev: {}, Prev:{}, Current: {} Pause: {}".format(self.sceneMan.secondPrevScence, self.sceneMan.prevScence, self.sceneMan.currentScene, self.paused))

g = Game()

while g.running:
    g.new()
print("End")
pg.quit()
