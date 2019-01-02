import pygame as pg
from settings import *
from sprites import *

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
        if self.level == "pause":
            self.pause()

    def level1(self):
        self.showPlayer = True
        Platform(self.game, 0, HEIGHT*7/8, WIDTH, HEIGHT/8, BLUE)
        Platform(self.game, WIDTH, HEIGHT*7/8, WIDTH, HEIGHT/8, GREEN)
        Platform(self.game, 2*WIDTH, HEIGHT*7/8, WIDTH, HEIGHT/8, BLUE)
        # pauseIMG = pg.transform.scale(self.game.pauseIMG, (30,30))
        # pauseIMGRect = pauseIMG.get_rect()
        # pauseIMGRect.center = (WIDTH*8/9, HEIGHT/12)
        # self.game.screen.blit(pauseIMG, pauseIMGRect)
        self.pauseButton = Button(self.game, "pause", WIDTH*8/9, HEIGHT*1/12, 30, 30, YELLOW, LIGHT_BLUE, "", 18,self.game.pauseIMGWhite, self.game.pauseIMGBlack)

    def pause(self):
        self.game.drawText("Pause Menu", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*3/8, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Main Menu")
        self.level1Button = Button(self.game, "level1", WIDTH*5/8, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Resume")

    def settingsMenu(self):
        self.game.drawText("Settings", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/9, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.startScreenButton = Button(self.game, "startScreen", WIDTH/4, HEIGHT*3/8, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "View Start Screen")

    def levelSelect(self):
        self.game.drawText("Select Level", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)
        self.level1Button = Button(self.game, "level1", WIDTH*1/2, HEIGHT*1/2, WIDTH/6, HEIGHT/12, YELLOW, LIGHT_BLUE, "Level One")

    def stats(self):
        self.game.drawText("View your statistics", 25, WHITE, WIDTH/2, HEIGHT*1/9, fontName=self.game.interfaceFont)
        self.mainMenuButton = Button(self.game, "mainMenu", WIDTH*1/8, HEIGHT*1/12, 60, 25, YELLOW, LIGHT_BLUE, "Back", 18)

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
                self.currentScene = button.tag
                if button.tag != 'level1':
                    self.image = pg.transform.scale(self.game.menuImages[self.currentScene], (WIDTH, HEIGHT))
                    rect = self.image.get_rect()
                    self.game.screen.blit(self.image, rect)
                if button.tag == "startScreen":
                    self.loadLevel('startScreen')
                if button.tag == "levelSelect":
                    self.loadLevel('levelSelect')
                if button.tag == "shop":
                    self.loadLevel('shop')
                if button.tag == 'mainMenu':
                    self.loadLevel('mainMenu')
                if button.tag == "settingsMenu":
                    self.loadLevel('settingsMenu')
                if button.tag == 'leaderboard':
                    self.loadLevel('leaderboard')
                if button.tag == 'stats':
                    self.loadLevel('stats')
                if button.tag == 'level1':
                    self.loadLevel('level1')
                if button.tag == 'pause':
                    self.loadLevel('pause')
                button.kill()
        if self.currentScene != "level1":
            self.showPlayer = False
