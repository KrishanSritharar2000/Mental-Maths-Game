import pygame as pg
from os import path
import random
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

        self.pauseScreen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.pauseScreenImage = pg.transform.scale(self.menuImages['pause'], (WIDTH, HEIGHT))
        self.pauseScreenImageRect = self.pauseScreenImage.get_rect()
        self.pauseScreen.blit(self.pauseScreenImage, self.pauseScreenImageRect)
        self.drawText("Pause Menu", 25, WHITE, WIDTH/2, HEIGHT*1/9, surf=self.pauseScreen, fontName=self.interfaceFont)    #wasnt being printed before because it was before the previous line
        self.pauseIMGWhite = pg.image.load(path.join(self.imgFolder, 'pauseWhite.png')).convert_alpha()
        self.pauseIMGBlack = pg.image.load(path.join(self.imgFolder, 'pauseBlack.png')).convert_alpha()

        self.playerBikeImage = pg.transform.scale(pg.image.load(path.join(self.imgFolder, 'bike.png')).convert_alpha(), (30, 30))

    def loadQuestions():
        questionFile = path.join(self.game_folder, 'questions.csv')
        with open(questions, 'r') as questionFile:
            reader = csv.reader(questionFile)
            next(questionFile)
            self.questionData=[]
            for line in reader:
                # line = [QuestionID, Questtion, CAns, WAns1, Wans2, Wans3, Wans4, Diff, level, isMaj]
                temp = []
                questionID = int(line[0])
                question = str(line[1])
                cAns = int(line[2])
                wAns1, wAns2, wAns3, wAns4 = int(line[3]),int(line[4]),int(line[5]),int(line[6])
                diff = str(line[7])
                level = int(line[8])
                isMaj = str(line[9])
                temp.extend((questionID,question,cAns,wAns1,wAns2,wAns3,wAns4,diff,level,isMaj))
                self.questionData.append(temp)#all the data is now held in a 2D array



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
        self.allSprites = pg.sprite.Group()#This groups all the sprties together
        self.buttons = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.rectangles = pg.sprite.Group()    #This is the area under the track
        self.map = None
        self.camera = None
        #Map(path.join(self.gameFolder,'map2.txt', 'LevelTest2'))
        #Camera(self.map.width, self.map.height)
        self.sceneMan = sceneManager(self)
        self.player = None
        self.paused = False
        self.pauseScreenPrinted = False
        self.prevRotate = 0
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
            if self.sceneMan.currentScene not in MENU_SCREENS:
                self.camera.update(self.player)

                hitPlatform = pg.sprite.spritecollide(self.player, self.platforms, False)
                if hitPlatform:
                    self.player.pos.y = hitPlatform[0].rect.y - self.player.height / 2
                    self.player.vel.y = 0

                    self.vecToPlayer = self.player.pos - vec(0, HEIGHT)
                    self.rotate = self.vecToPlayer.angle_to(vec(1, 0))
                    # print(self.player.pos)
                    # print(self.rotate)
                    if self.prevRotate != round(self.rotate,2):
                        self.player.image = self.rot_center(self.player.image, self.rotate)
                        # self.player.image = pg.transform.rotate(self.player.image, self.rotate)
                        # self.player.rect = self.player.image.get_rect()
                        # self.player.rect.center = self.player.pos
                        self.prevRotate = round(self.rotate,2)

    def events(self):
        #Game loop - Events1
        for event in pg.event.get():
            #check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                    if self.paused == False:
                        for button in self.buttons:
                            button.kill()
                    self.pauseScreenPrinted = False


                    # self.currentScene = self.sceneManPrevScence

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        if self.paused:
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
            if self.sceneMan.currentScene not in MENU_SCREENS:
                for sprite in self.allSprites:
                    self.screen.blit(sprite.image, self.camera.applyOffset(sprite))
        pg.display.flip()



        #used for buffered frames- ALWAYS DO THIS LAST AFTER DRAWING EVERYTHING




        # print('paused', self.paused)
        print("self.buttons", self.buttons, self.paused, self.sceneMan.currentScene )
        print("2nd Prev: {}, Prev:{}, Current: {} Pause: {}".format(self.sceneMan.secondPrevScence, self.sceneMan.prevScence, self.sceneMan.currentScene, self.paused))

        # for button in self.buttons:
        #     print(button.tag)


g = Game()

while g.running:
    g.new()

pg.quit()
